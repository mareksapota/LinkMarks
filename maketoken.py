#!/usr/bin/env python

from __future__ import print_function

import sys
import model

if len(sys.argv) == 1:
    print("No args given.")
    sys.exit(1)

permanent = False
token = sys.argv[1]

if len(sys.argv) > 2 and sys.argv[1] == "permanent":
    permanent = True
    token = sys.argv[2]

model.Token.save(token, permanent)

print("Saved", "permanent" if permanent else "temporary", "token:")
print(token)
