#!/bin/bash

check_game_timestamps() {
  L1_RPC="http://130.60.144.77:8549"

  # Prompt for GAME address
  read -rp "Enter GAME contract address: " GAME
  if [ -z "$GAME" ]; then
    echo "Error: GAME contract address is required." >&2
    return 1
  fi

  echo "Finding contract creation block for $GAME..."

  # Get latest block number (decimal)
  LATEST_BLOCK_HEX=$(cast block latest --rpc-url "$L1_RPC" --json | jq -r '.number')
  LATEST_BLOCK=$((LATEST_BLOCK_HEX))

  START_BLOCK=0
  END_BLOCK=$LATEST_BLOCK
  CREATION_BLOCK=-1

  # Binary search for creation block
  while [ "$START_BLOCK" -le "$END_BLOCK" ]; do
    MID=$(((START_BLOCK + END_BLOCK) / 2))
    # Check code at MID block
    CODE=$(cast code "$GAME" --rpc-url "$L1_RPC" --block "$MID" 2>/dev/null)
    if [ -z "$CODE" ] || [ "$CODE" = "0x" ]; then
      # No code yet, move forward
      START_BLOCK=$((MID + 1))
    else
      # Code exists, contract deployed at or before MID
      CREATION_BLOCK=$MID
      END_BLOCK=$((MID - 1))
    fi
  done

  if [ "$CREATION_BLOCK" -eq -1 ]; then
    echo "Error: Could not find creation block for contract $GAME" >&2
    return 1
  fi

  echo "Contract creation block found: $CREATION_BLOCK"

  # 1) Block timestamp at creation
  TS0_HEX=$(cast block "$CREATION_BLOCK" --rpc-url "$L1_RPC" --json | jq -r '.timestamp' 2>/dev/null)
  if [ -z "$TS0_HEX" ] || [ "$TS0_HEX" = "null" ]; then
    echo "Warning: Could not read timestamp for block $CREATION_BLOCK" >&2
    return 1
  fi
  TS0=$((TS0_HEX))

  # 2) Current block timestamp
  TS_NOW_HEX=$(cast block latest --rpc-url "$L1_RPC" --json | jq -r '.timestamp' 2>/dev/null)
  if [ -z "$TS_NOW_HEX" ] || [ "$TS_NOW_HEX" = "null" ]; then
    echo "Warning: Could not read current timestamp" >&2
    return 1
  fi
  TS_NOW=$((TS_NOW_HEX))

  # 3) Elapsed seconds since creation
  if [ "$TS_NOW" -le "$TS0" ]; then
    ELAPSED=0
  else
    ELAPSED=$((TS_NOW - TS0))
  fi

  # 4) Total allowed window from the game (maxClockDuration)
  MAX=$(cast call "$GAME" 'maxClockDuration()(uint64)' --rpc-url "$L1_RPC" 2>/dev/null)
  if [ -z "$MAX" ]; then
    echo "Warning: Could not read maxClockDuration from contract $GAME" >&2
    return 1
  fi

  # 5) Remaining = max(0, MAX - ELAPSED)
  if [ "$ELAPSED" -ge "$MAX" ]; then
    REM=0
  else
    REM=$((MAX - ELAPSED))
  fi

  echo "created_at: $(date -d @"$TS0" 2>/dev/null || echo "$TS0")"
  echo "now:        $(date -d @"$TS_NOW" 2>/dev/null || echo "$TS_NOW")"
  echo "elapsed:    ${ELAPSED}s  (~$((ELAPSED/60)) minutes)"
  echo "max:        ${MAX}s     (~$((MAX/60)) minutes)"
  echo "remaining:  ${REM}s     (~$((REM/60)) minutes)"

  return 0
}

# Call the function
check_game_timestamps