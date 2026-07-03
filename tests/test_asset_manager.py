import sys
from pathlib import Path

import pytest
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.assets import AssetManager


def test_load_texture_from_png(tmp_path: Path) -> None:
    image_path = tmp_path / "tile.png"
    Image.new("RGBA", (4, 4), (255, 0, 0, 255)).save(image_path)

    manager = AssetManager(search_paths=[str(tmp_path)])
    asset = manager.load_texture("tile.png")

    assert asset is not None
    assert asset.name == "tile"
    assert asset.size == (4, 4)
    assert asset.mode == "RGBA"


def test_load_mesh_from_obj(tmp_path: Path) -> None:
    mesh_path = tmp_path / "cube.obj"
    mesh_path.write_text(
        """v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 1.0 1.0 0.0
v 0.0 1.0 0.0
f 1 2 3
f 1 3 4
"""
    )

    manager = AssetManager(search_paths=[str(tmp_path)])
    asset = manager.load_mesh("cube.obj")

    assert asset is not None
    assert asset.name == "cube"
    assert len(asset.vertices) == 4
    assert len(asset.faces) == 2
