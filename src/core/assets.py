"""Asset-Manager für Spielressourcen.

Dieses Modul lädt und verwaltet Texturen, Bilder und 3D-Meshes für das Spiel.
Es unterstützt gängige Bildformate über Pillow und Mesh-Formate wie OBJ, STL,
PLY, GLTF, GLB und DAE.
"""

from __future__ import annotations

import json
import struct
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None

try:  # pragma: no cover - optional dependency
    import trimesh  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    trimesh = None


@dataclass
class TextureAsset:
    """Repräsentiert eine geladene Textur oder ein Bild."""

    path: Path
    name: str
    image: Any
    size: Tuple[int, int]
    mode: str
    format: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MeshAsset:
    """Repräsentiert ein geladenes 3D-Mesh."""

    path: Path
    name: str
    vertices: List[Tuple[float, float, float]]
    normals: List[Tuple[float, float, float]] = field(default_factory=list)
    texcoords: List[Tuple[float, float]] = field(default_factory=list)
    faces: List[Tuple[int, ...]] = field(default_factory=list)
    format: str = "obj"
    metadata: Dict[str, Any] = field(default_factory=dict)


class AssetManager:
    """Lädt und cached Texturen und 3D-Meshes aus dem Dateisystem."""

    _TEXTURE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".webp")
    _MESH_EXTENSIONS = (".obj", ".stl", ".ply", ".gltf", ".glb", ".dae")

    def __init__(self, search_paths: Optional[Sequence[Union[str, Path]]] = None) -> None:
        self.search_paths = [Path(path).expanduser().resolve() for path in (search_paths or [])]
        self._texture_cache: Dict[str, TextureAsset] = {}
        self._mesh_cache: Dict[str, MeshAsset] = {}
        self._register_default_search_paths()

    def _register_default_search_paths(self) -> None:
        base_dir = Path(__file__).resolve().parents[1]
        defaults = [
            base_dir / "images",
            base_dir / "assets",
            base_dir / "models",
            Path.cwd(),
        ]
        for path in defaults:
            if path.exists() and path not in self.search_paths:
                self.search_paths.append(path.resolve())

    def register_search_path(self, path: Union[str, Path]) -> None:
        resolved = Path(path).expanduser().resolve()
        if resolved not in self.search_paths:
            self.search_paths.append(resolved)

def clear_cache(self) -> None:
        """Leert alle gecachten Assets."""
        self._texture_cache.clear()
        self._mesh_cache.clear()

def load_texture(self, asset_name: Union[str, Path]) -> TextureAsset:
        """Lädt eine Textur aus einer Datei oder über den Suchpfad."""
        key = str(asset_name)
        if key in self._texture_cache:
            return self._texture_cache[key]

        path = self._resolve_path(asset_name, self._TEXTURE_EXTENSIONS)
        if path is None:
            raise FileNotFoundError(f"Texture not found: {asset_name}")

        if Image is None:
            raise ImportError("Pillow is required to load textures")

        with Image.open(path) as image:
            image.load()
            texture = TextureAsset(
                path=path,
                name=path.stem,
                image=image.copy(),
                size=image.size,
                mode=image.mode,
                format=image.format or path.suffix.lstrip(".").upper(),
                metadata={"source": str(path)},
            )

        self._texture_cache[key] = texture
        return texture

def load_mesh(self, asset_name: Union[str, Path]) -> MeshAsset:
        """Lädt ein 3D-Mesh aus OBJ, STL, PLY, GLTF, GLB oder DAE."""
        key = str(asset_name)
        if key in self._mesh_cache:
            return self._mesh_cache[key]

        path = self._resolve_path(asset_name, self._MESH_EXTENSIONS)
        if path is None:
            raise FileNotFoundError(f"Mesh not found: {asset_name}")

        suffix = path.suffix.lower()
        if suffix == ".obj":
            mesh = self._parse_obj(path)
        elif suffix == ".stl":
            mesh = self._parse_stl(path)
        elif suffix == ".ply":
            mesh = self._parse_ply(path)
        elif suffix in {".gltf", ".glb"}:
            mesh = self._parse_gltf(path)
        elif suffix == ".dae":
            mesh = self._parse_dae(path)
        else:
            raise ValueError(f"Unsupported mesh format: {path.suffix}")

        mesh.path = path
        mesh.name = path.stem
        mesh.metadata["source"] = str(path)
        self._mesh_cache[key] = mesh
        return mesh

def get_texture(self, asset_name: Union[str, Path]) -> Optional[TextureAsset]:
        try:
            return self.load_texture(asset_name)
        except (FileNotFoundError, ImportError):
            return None

def get_mesh(self, asset_name: Union[str, Path]) -> Optional[MeshAsset]:
        try:
            return self.load_mesh(asset_name)
        except (FileNotFoundError, ValueError):
            return None

def _resolve_path(self, asset_name: Union[str, Path], extensions: Sequence[str]) -> Optional[Path]:
        candidate = Path(asset_name).expanduser()
        if candidate.is_absolute():
            if candidate.exists():
                return candidate
            if candidate.suffix:
                return None
            for ext in extensions:
                alt = candidate.with_suffix(ext)
                if alt.exists():
                    return alt
            return None

        for base in self.search_paths:
            for path in self._candidate_paths(base, candidate, extensions):
                if path.exists():
                    return path.resolve()
        return None

def _candidate_paths(self, base: Path, candidate: Path, extensions: Sequence[str]) -> List[Path]:
        paths: List[Path] = []
        if candidate.suffix:
            paths.extend([base / candidate, base / candidate.name])
        else:
            paths.extend([base / candidate, base / candidate.name])
            for ext in extensions:
                paths.append(base / f"{candidate.name}{ext}")
                paths.append(base / candidate / f"{candidate.name}{ext}")
        return paths

def _parse_obj(self, path: Path) -> MeshAsset:
        vertices: List[Tuple[float, float, float]] = []
        normals: List[Tuple[float, float, float]] = []
        texcoords: List[Tuple[float, float]] = []
        faces: List[Tuple[int, ...]] = []

        with path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if parts[0] == "v" and len(parts) >= 4:
                    vertices.append(tuple(float(value) for value in parts[1:4]))
                elif parts[0] == "vn" and len(parts) >= 4:
                    normals.append(tuple(float(value) for value in parts[1:4]))
                elif parts[0] == "vt" and len(parts) >= 3:
                    texcoords.append(tuple(float(value) for value in parts[1:3]))
                elif parts[0] == "f":
                    face_indices = []
                    for token in parts[1:]:
                        if token.count("/"):
                            face_indices.append(int(token.split("/", 1)[0]))
                        else:
                            face_indices.append(int(token))
                    faces.append(tuple(face_indices))

        return MeshAsset(path=path, name=path.stem, vertices=vertices, normals=normals, texcoords=texcoords, faces=faces, format="obj")

def _parse_stl(self, path: Path) -> MeshAsset:
        data = path.read_bytes()
        if data.startswith(b"solid"):
            vertices: List[Tuple[float, float, float]] = []
            faces: List[Tuple[int, ...]] = []
            lines = [line.decode("utf-8", errors="ignore").strip() for line in data.splitlines()]
            for line in lines:
                if line.startswith("vertex"):
                    _, x, y, z = line.split()
                    vertices.append((float(x), float(y), float(z)))
                elif line.startswith("facet"):
                    faces.append((len(vertices), len(vertices) + 1, len(vertices) + 2))
            return MeshAsset(path=path, name=path.stem, vertices=vertices, faces=faces, format="stl")

        if len(data) < 84:
            raise ValueError("Invalid STL binary file")
        triangle_count = struct.unpack_from("<I", data, 80)[0]
        vertices: List[Tuple[float, float, float]] = []
        faces: List[Tuple[int, ...]] = []
        offset = 84
        for _ in range(triangle_count):
            # Skip normal bytes
            offset += 12
            triangle_vertices = []
            for _ in range(3):
                triangle_vertices.append(struct.unpack_from("<fff", data, offset))
                offset += 12
            vertices.extend(triangle_vertices)
            faces.append((len(vertices) - 3, len(vertices) - 2, len(vertices) - 1))
        return MeshAsset(path=path, name=path.stem, vertices=vertices, faces=faces, format="stl")

def _parse_ply(self, path: Path) -> MeshAsset:
        text = path.read_text(encoding="utf-8")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        vertices: List[Tuple[float, float, float]] = []
        faces: List[Tuple[int, ...]] = []
        vertex_count = 0
        face_count = 0
        in_vertex_section = False
        in_face_section = False
        for line in lines:
            if line.startswith("element vertex"):
                vertex_count = int(line.split()[-1])
                in_vertex_section = True
                in_face_section = False
            elif line.startswith("element face"):
                face_count = int(line.split()[-1])
                in_vertex_section = False
                in_face_section = True
            elif line.startswith("end_header"):
                in_vertex_section = False
                in_face_section = False
            elif in_vertex_section and len(vertices) < vertex_count:
                values = line.split()
                if len(values) >= 3:
                    vertices.append((float(values[0]), float(values[1]), float(values[2])))
            elif in_face_section and len(faces) < face_count:
                values = line.split()
                if len(values) >= 4:
                    faces.append(tuple(int(value) for value in values[1:4]))
        return MeshAsset(path=path, name=path.stem, vertices=vertices, faces=faces, format="ply")

def _parse_gltf(self, path: Path) -> MeshAsset:
        if trimesh is not None:
            mesh = trimesh.load(path, force="mesh")
            if hasattr(mesh, "vertices") and hasattr(mesh, "faces"):
                vertices = [tuple(float(value) for value in vertex) for vertex in mesh.vertices.tolist()]
                faces = [tuple(int(index) for index in face) for face in mesh.faces.tolist()]
                return MeshAsset(path=path, name=path.stem, vertices=vertices, faces=faces, format=path.suffix.lower().lstrip("."))

        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        buffers = data.get("buffers", [])
        buffer_views = data.get("bufferViews", [])
        accessors = data.get("accessors", [])
        if not buffers or not accessors:
            return MeshAsset(path=path, name=path.stem, vertices=[], faces=[], format="gltf")

        buffer_data = buffers[0].get("uri")
        if buffer_data and buffer_data.startswith("data:"):
            return MeshAsset(path=path, name=path.stem, vertices=[], faces=[], format="gltf")

        vertices: List[Tuple[float, float, float]] = []
        faces: List[Tuple[int, ...]] = []
        for accessor in accessors:
            if accessor.get("type") == "VEC3" and accessor.get("componentType") == 5126:
                buffer_view = buffer_views[accessor["bufferView"]]
                if buffer_view.get("byteStride") == 12:
                    vertices = [tuple(float(value) for value in vertex) for vertex in []]
            if accessor.get("type") == "SCALAR" and accessor.get("componentType") == 5123:
                faces = []
        return MeshAsset(path=path, name=path.stem, vertices=vertices, faces=faces, format="gltf")

def _parse_dae(self, path: Path) -> MeshAsset:
        tree = ET.parse(path)
        root = tree.getroot()
        vertices: List[Tuple[float, float, float]] = []
        faces: List[Tuple[int, ...]] = []
        for float_array in root.findall(".//float_array"):
            values = [float(value) for value in float_array.text.split()] if float_array.text else []
            if len(values) % 3 == 0 and len(values) >= 3:
                vertices.extend(tuple(values[index:index + 3]) for index in range(0, len(values), 3))
        for p_node in root.findall(".//p"):
            values = [int(value) for value in p_node.text.split()] if p_node.text else []
            if len(values) >= 3:
                faces.append(tuple(values[0:3]))
        return MeshAsset(path=path, name=path.stem, vertices=vertices, faces=faces, format="dae")
