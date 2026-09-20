"""Diagnostic import through Sollumz's own Blender importer."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "work/blender-site"))

import bpy
import Sollumz
import Sollumz.sollumz_preferences as sollumz_preferences
import mathutils
import szio.types
class _DiagnosticPreferences:
    use_text_name_as_mat_name = False
    show_version_in_statusbar = False
    shared_textures_directories = ()
    hidden_panels = ()
    default_sync_selection_enabled = False

    def __getattr__(self, name):
        return () if name.endswith(("paths", "directories", "panels")) else False

sollumz_preferences.get_addon_preferences = lambda context=None: _DiagnosticPreferences()
szio.types.use_math_types(mathutils.Vector, mathutils.Quaternion, mathutils.Matrix)
auto = Sollumz.auto_load
auto.modules = auto.get_all_submodules(Path(Sollumz.__file__).parent, Sollumz.__package__)
auto.ordered_classes = auto.get_ordered_classes_to_register(auto.modules)
for pre_register in auto.iter_module_functions("pre_register_classes"):
    pre_register(auto.ordered_classes)
for cls in auto.ordered_classes:
    bpy.utils.register_class(cls)
for register in auto.iter_module_functions("register"):
    try:
        register()
    except Exception as exc:
        print("SOLLUMZ_OPTIONAL_REGISTER_SKIPPED", register.__module__, repr(exc))
from szio.gta5 import try_load_asset
from Sollumz.yft.yftimport import create_fragment
from Sollumz.iecontext import ImportContext, ImportSettings, import_context_scope

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

folder = ROOT / "work/source-extracted/x64/vehicles.extracted"
frag, target = try_load_asset(folder / "fusion.yft", return_target=True)
hi_frag = try_load_asset(folder / "fusion_hi.yft")
settings = ImportSettings(import_as_asset=False, split_by_group=False,
                          mlo_instance_entities=False, map_instance_entities=False)
ctx = ImportContext("fusion", target, folder, settings)
with import_context_scope(ctx):
    obj = create_fragment(frag, hi_frag, "fusion", None, None)

bpy.context.view_layer.objects.active = obj
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "blender/source-sollumz.blend"))
print("SOLLUMZ_IMPORT_READY", len(bpy.data.objects), len(bpy.data.meshes))
