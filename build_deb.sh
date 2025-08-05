#!/usr/bin/env bash
set -euo pipefail

# Simple Debian package builder for Apophis
# Usage: ./build_deb.sh

NAME=apophis
VERSION=$(python3 - <<'PY'
import re, pathlib
text = pathlib.Path('pyproject.toml').read_text()
m = re.search(r'^version = "([^"]+)"', text, re.MULTILINE)
print(m.group(1) if m else '0')
PY
)
WORKDIR=build/deb

rm -rf "$WORKDIR" "${NAME}_${VERSION}.deb"
mkdir -p "$WORKDIR/DEBIAN" \
         "$WORKDIR/usr/lib/python3/dist-packages" \
         "$WORKDIR/usr/bin" \
         "$WORKDIR/usr/share/applications"

cat > "$WORKDIR/DEBIAN/control" <<CONTROL
Package: $NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: python3
Maintainer: Apophis Developers
Description: Apophis language utilities with IDE
CONTROL

# Install python modules
cp apophis.py apophis_ide.py "$WORKDIR/usr/lib/python3/dist-packages/"

# CLI launcher for the IDE
cat > "$WORKDIR/usr/bin/apophis-ide" <<'LAUNCH'
#!/usr/bin/env python3
from apophis_ide import launch
launch()
LAUNCH
chmod +x "$WORKDIR/usr/bin/apophis-ide"

# Desktop entry for menu systems
cat > "$WORKDIR/usr/share/applications/apophis.desktop" <<'DESKTOP'
[Desktop Entry]
Type=Application
Name=Apophis
Comment=Apophis IDE
Exec=apophis-ide
Terminal=false
Categories=Development;
DESKTOP
chmod 644 "$WORKDIR/usr/share/applications/apophis.desktop"

dpkg-deb --build "$WORKDIR" "${NAME}_${VERSION}.deb"

echo "Created ${NAME}_${VERSION}.deb"
