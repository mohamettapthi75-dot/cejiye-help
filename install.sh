#!/bin/bash
echo '#!/usr/bin/env python3' | cat - cejiye.py > ~/cejiye_temp
mv ~/cejiye_temp $PREFIX/bin/cejiye
chmod +x $PREFIX/bin/cejiye
echo "✅ cejiye si guul leh ayaa la rakibay!"
