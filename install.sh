#!/bin/bash
echo '#!/usr/bin/env python3' > /tmp/cejiye_temp
cat cejiye.py >> /tmp/cejiye_temp
cp /tmp/cejiye_temp $PREFIX/bin/cejiye
chmod +x $PREFIX/bin/cejiye
echo "✅ cejiye si guul leh ayaa la rakibay!"
