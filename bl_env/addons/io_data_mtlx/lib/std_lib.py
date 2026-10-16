# Copyright (c) 2026 Activision Publishing, Inc. and contributors. All Rights Reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import os
import bpy
import MaterialX as mx
from .node_registry import register_materialx_node
from .graph_utils import (
    apply_default_values,
    create_blender_node,
    blender_from_color4_bundle,
    blender_from_vector4_bundle,
    blender_to_color4_bundle,
    blender_to_vector4_bundle,
    )


@register_materialx_node("ND_texcoord_vector2")
def ND_texcoord_vector2(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeUVMap)

    mx_node_inputs = {}
    # No inputs for texcoord node
    # see if we can get the name of the uv map from the mx_node's index?
    # index = mx_node.getInput('index')
    # node.uv_map = "UVMap"

    mx_node_outputs = {"out": node.outputs["UV"]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_divide_vector2")
def ND_divide_vector2(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)

    node.operation = 'DIVIDE'
    node.update()
    node.inputs[0].default_value = (0.0, 0.0, 0.0)  # Default vector value
    node.inputs[1].default_value = (1.0, 1.0, 1.0)  # Default vector value

    mx_node_inputs = {}
    mx_node_inputs["in1"] = node.inputs[0]
    mx_node_inputs["in2"] = node.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


# MaterialX colorspace names to Blender's. Colour images without one use the document's.
MX_TO_BLENDER_COLORSPACE = {
    "srgb_texture": "sRGB",
    "lin_rec709": "Linear Rec.709",
    "acescg": "ACEScg",
    "lin_ap1": "ACEScg",
    "raw": "Non-Color",
}


def _image_colorspace(mx_node: mx.Node, is_color: bool) -> str:
    if not is_color:
        return "Non-Color"
    file_input = mx_node.getInput("file")
    space = file_input.getColorSpace() or mx_node.getActiveColorSpace()
    if not space:
        return "sRGB"
    if space not in MX_TO_BLENDER_COLORSPACE:
        raise ValueError(f"{mx_node.getNamePath()}: unsupported colorspace '{space}'")
    return MX_TO_BLENDER_COLORSPACE[space]


def _load_image(image_path: str, colorspace: str) -> bpy.types.Image:
    """Load once per (file, colorspace), so one file read as colour and as data keeps both."""
    if not os.path.exists(image_path):
        bl_image = bpy.data.images.new(name=image_path, width=1, height=1)
        bl_image.generated_color = (0.0, 0.0, 0.0, 0.0)  # Default color if image not found
        return bl_image
    abs_path = os.path.normpath(bpy.path.abspath(image_path))
    for bl_image in bpy.data.images:
        if (os.path.normpath(bpy.path.abspath(bl_image.filepath)) == abs_path
                and bl_image.colorspace_settings.name == colorspace):
            return bl_image
    bl_image = bpy.data.images.load(image_path, check_existing=False)
    bl_image.colorspace_settings.name = colorspace
    return bl_image


def _image(tree: bpy.types.NodeTree, mx_node: mx.Node, is_color: bool):
    image_path = mx_node.getInput("file").getValueString()
    node: bpy.types.ShaderNodeTexImage = create_blender_node(tree, mx_node, bpy.types.ShaderNodeTexImage)
    node.image = _load_image(image_path, _image_colorspace(mx_node, is_color))
    node.interpolation = 'Linear'

    mx_node_inputs = {}
    mx_node_inputs["texcoord"] = node.inputs['Vector']

    apply_default_values(mx_node, mx_node_inputs)
    return node, mx_node_inputs


@register_materialx_node("ND_image_color3")
def ND_image_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node, mx_node_inputs = _image(tree, mx_node, is_color=True)
    mx_node_outputs = {"out": node.outputs['Color']}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_image_vector3")
def ND_image_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node, mx_node_inputs = _image(tree, mx_node, is_color=False)
    mx_node_outputs = {"out": node.outputs['Color']}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_image_float")
def ND_image_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node, mx_node_inputs = _image(tree, mx_node, is_color=False)
    split_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeSeparateColor)
    tree.links.new(split_node.inputs[0], node.outputs['Color'])
    mx_node_outputs = {"out": split_node.outputs[0]}
    return (node, split_node), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_multiply_vector2")
def ND_multiply_vector2(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)

    node.operation = 'MULTIPLY'
    node.update()
    node.inputs[0].default_value = (0.0, 0.0, 0.0)  # Default vector value
    node.inputs[1].default_value = (1.0, 1.0, 1.0)  # Default vector value

    mx_node_inputs = {}
    mx_node_inputs["in1"] = node.inputs[0]
    mx_node_inputs["in2"] = node.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_subtract_vector2")
def ND_subtract_vector2(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)

    node.operation = 'SUBTRACT'
    node.update()
    node.inputs[0].default_value = (0.0, 0.0, 0.0)  # Default vector value
    node.inputs[1].default_value = (0.0, 0.0, 0.0)  # Default vector value

    mx_node_inputs = {}
    mx_node_inputs["in1"] = node.inputs[0]
    mx_node_inputs["in2"] = node.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_ifequal_floatB")
def ND_ifequal_floatB(tree: bpy.types.NodeTree, mx_node: mx.Node):
    """Create a Blender node network that represents the MaterialX ND_ifequal_floatB node.
    ```
    ╔════════════════╗       ╔════════════════╗
    ║ Compare Node   ║       ║ Mix Node       ║
    ║           Value╠───┐   ║          Result╠
    ║ [ ] Clamp      ║   │   ║ Float          ║
    ╣ Value          ║   │   ║ [█] Clamp      ║
    ╣ Value          ║   └───╣ Factor         ║
    ╣ Epsilon = 0.0  ║       ╣ A              ║
    ╚════════════════╝       ╣ B              ║
                             ╚════════════════╝
    ```
    """
    compare_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    compare_node.operation = 'COMPARE'
    compare_node.inputs[0].default_value = 0.0  # First value
    compare_node.inputs[1].default_value = 0.0  # Second value
    compare_node.inputs[2].default_value = 0.0  # Epsilon value
    compare_node.update()

    mix_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMix)
    mix_node.update()
    mix_node.inputs[2].default_value = 0.0  # False
    mix_node.inputs[3].default_value = 0.0  # False
    tree.links.new(mix_node.inputs[0], compare_node.outputs[0])

    mx_node_inputs = {}
    mx_node_inputs["value1"] = compare_node.inputs[0]
    mx_node_inputs["value2"] = compare_node.inputs[1]
    mx_node_inputs["in1"] = mix_node.inputs[2]
    mx_node_inputs["in2"] = mix_node.inputs[3]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": mix_node.outputs[0]}
    return (compare_node, mix_node), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_ifequal_color3B")
def ND_ifequal_color3B(tree: bpy.types.NodeTree, mx_node: mx.Node):
    """Create a Blender node network that represents the MaterialX ND_ifequal_color3B node.
    ```
    ╔════════════════╗       ╔════════════════╗
    ║ Compare Node   ║       ║ Mix Node       ║
    ║           Value╠───┐   ║          Result╠
    ║ [ ] Clamp      ║   │   ║ Color / Mix    ║
    ╣ Value          ║   │   ║ [█] Clamp      ║
    ╣ Value          ║   └───╣ Factor         ║
    ╣ Epsilon = 0.0  ║       ╣ A              ║
    ╚════════════════╝       ╣ B              ║
                             ╚════════════════╝
    ```
    """
    compare_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    compare_node.operation = 'COMPARE'
    compare_node.inputs[0].default_value = 0.0  # First value
    compare_node.inputs[1].default_value = 0.0  # Second value
    compare_node.inputs[2].default_value = 0.0  # Epsilon value
    compare_node.update()

    mix_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMixRGB)
    mix_node.inputs[1].default_value = [0.0, 0.0, 0.0, 1.0]
    mix_node.inputs[2].default_value = [0.0, 0.0, 0.0, 1.0]
    mix_node.update()
    tree.links.new(mix_node.inputs[0], compare_node.outputs[0])

    mx_node_inputs = {}
    mx_node_inputs["value1"] = compare_node.inputs[0]
    mx_node_inputs["value2"] = compare_node.inputs[1]
    mx_node_inputs["in1"] = mix_node.inputs[1]
    mx_node_inputs["in2"] = mix_node.inputs[2]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": mix_node.outputs[0]}
    return (compare_node, mix_node), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_ifequal_vector3B")
def ND_subtract_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    node.operation = 'SUBTRACT'
    node.inputs[0].default_value = 0.0  # Default value for input 1
    node.inputs[1].default_value = 0.0  # Default value for input 2

    mx_node_inputs = {}
    mx_node_inputs["in1"] = node.inputs[0]
    mx_node_inputs["in2"] = node.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_multiply_float")
def ND_multiply_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    node.operation = 'MULTIPLY'
    node.update()
    node.inputs[0].default_value = 0.0  # Default factor for multiplication
    node.inputs[1].default_value = 1.0  # Default factor for multiplication

    mx_node_inputs = {}
    mx_node_inputs["in1"] = node.inputs[0]
    mx_node_inputs["in2"] = node.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


# @register_materialx_node("ND_distance_float")
# def ND_distance_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
#     node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
#     node.operation = 'DISTANCE'

#     mx_node_inputs = {}
#     mx_node_inputs["in1"] = node.inputs[0]
#     mx_node_inputs["in2"] = node.inputs[1]

#     mx_node_outputs = {"out": node.outputs[0]}
#     return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_mix_vector3")
def ND_mix_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMix)
    node.data_type = 'VECTOR'
    node.factor_mode = 'UNIFORM'
    node.update()
    node.inputs["A"].default_value = (0.0, 0.0, 0.0)
    node.inputs["B"].default_value = (0.0, 0.0, 0.0)
    node.inputs["Factor"].default_value = 0.0

    mx_node_inputs = {}
    mx_node_inputs["fg"] = node.inputs["A"]
    mx_node_inputs["bg"] = node.inputs["B"]
    mx_node_inputs["mix"] = node.inputs["Factor"]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs["Result"]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_convert_vector4_vector3")
def ND_convert_vector4_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    # if vector4 is an input, we have to also spawn an input of constants here
    vec4_input = blender_from_vector4_bundle(tree, mx_node, bpy.types.NodeReroute)
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineXYZ)
    tree.links.new(vec4_input.outputs[0], node.inputs[0])
    tree.links.new(vec4_input.outputs[1], node.inputs[1])
    tree.links.new(vec4_input.outputs[2], node.inputs[2])

    mx_node_inputs = {}
    mx_node_inputs["in"] = vec4_input.inputs[0]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_tiledimage_vector4")
def ND_tiledimage_vector4(tree: bpy.types.NodeTree, mx_node: mx.Node):
    file_input = mx_node.getInput("file")
    image_path = file_input.getValueString()
    node: bpy.types.ShaderNodeTexImage = create_blender_node(tree, mx_node, bpy.types.ShaderNodeTexImage)
    if os.path.exists(image_path):
        bl_image = bpy.data.images.load(image_path, check_existing=True)
    else:
        bl_image = bpy.data.images.new(name=image_path, width=1, height=1)
        bl_image.generated_color = (0.0, 0.0, 0.0, 0.0)  # Default color if image not found
    # use suffix of image_path?
    bl_image.colorspace_settings.name = 'Linear Rec.709'  # Assuming the image is in Rec.709 color space
    node.image = bl_image
    # node.colorspace_settings.name = 'Linear Rec.709'
    node.interpolation = 'Linear'
    uv_map = create_blender_node(tree, mx_node, bpy.types.ShaderNodeUVMap)
    uv_tiling = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    uv_tiling.operation = 'MULTIPLY'
    uv_tiling.inputs[1].default_value = (1.0, 1.0, 1.0)  # Tiling factor
    uv_offset = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    uv_offset.operation = 'ADD'
    tree.links.new(node.inputs[0], uv_offset.outputs[0])  # Connect UV offset to image node
    tree.links.new(uv_tiling.inputs[0], uv_map.outputs[0])
    tree.links.new(uv_offset.inputs[0], uv_tiling.outputs[0])
    split_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeSeparateXYZ)
    bundle = blender_to_vector4_bundle(tree, mx_node, bpy.types.NodeCombineBundle)
    tree.links.new(split_node.inputs[0], node.outputs[0]) # RGB to split
    tree.links.new(bundle.inputs[0], split_node.outputs[0]) # X
    tree.links.new(bundle.inputs[1], split_node.outputs[1]) # Y
    tree.links.new(bundle.inputs[2], split_node.outputs[2]) # Z
    tree.links.new(bundle.inputs[3], node.outputs[1]) # (Alpha)

    mx_node_inputs = {}
    mx_node_inputs["texcoord"] = uv_tiling.inputs[0] # by default connected to uv_map node defined above
    mx_node_inputs["uvtiling"] = uv_tiling.inputs[1]
    mx_node_inputs["uvoffset"] = uv_offset.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": bundle.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_tiledimage_color4")
def ND_tiledimage_color4(tree: bpy.types.NodeTree, mx_node: mx.Node):
    file_input = mx_node.getInput("file")
    image_path = file_input.getValueString()
    node: bpy.types.ShaderNodeTexImage = create_blender_node(tree, mx_node, bpy.types.ShaderNodeTexImage)
    if os.path.exists(image_path):
        bl_image = bpy.data.images.load(image_path, check_existing=True)
    else:
        bl_image = bpy.data.images.new(name=image_path, width=1, height=1)
        bl_image.generated_color = (0.0, 0.0, 0.0, 0.0)  # Default color if image not found
    # use suffix of image_path?
    bl_image.colorspace_settings.name = 'sRGB'  # Assuming the image is in sRGB color space
    node.image = bl_image
    # node.colorspace_settings.name = 'Linear Rec.709'
    node.interpolation = 'Linear'
    uv_map = create_blender_node(tree, mx_node, bpy.types.ShaderNodeUVMap)
    uv_tiling = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    uv_tiling.operation = 'MULTIPLY'
    uv_tiling.inputs[1].default_value = (1.0, 1.0, 1.0)  # Tiling factor
    uv_offset = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    uv_offset.operation = 'ADD'
    tree.links.new(node.inputs[0], uv_offset.outputs[0])  # Connect UV offset to image node
    tree.links.new(uv_tiling.inputs[0], uv_map.outputs[0])
    tree.links.new(uv_offset.inputs[0], uv_tiling.outputs[0])
    split_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeSeparateXYZ)
    bundle = blender_to_color4_bundle(tree, mx_node, bpy.types.NodeCombineBundle)
    tree.links.new(split_node.inputs[0], node.outputs[0]) # RGB to split
    tree.links.new(bundle.inputs[0], split_node.outputs[0]) # X
    tree.links.new(bundle.inputs[1], split_node.outputs[1]) # Y
    tree.links.new(bundle.inputs[2], split_node.outputs[2]) # Z
    tree.links.new(bundle.inputs[3], node.outputs[1]) # (Alpha)

    mx_node_inputs = {}
    mx_node_inputs["texcoord"] = uv_tiling.inputs[0] # by default connected to uv_map node defined above
    mx_node_inputs["uvtiling"] = uv_tiling.inputs[1]
    mx_node_inputs["uvoffset"] = uv_offset.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": bundle.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_tiledimage_float")
def ND_tiledimage_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    file_input = mx_node.getInput("file")
    image_path = file_input.getValueString()
    node: bpy.types.ShaderNodeTexImage = create_blender_node(tree, mx_node, bpy.types.ShaderNodeTexImage)
    if os.path.exists(image_path):
        bl_image = bpy.data.images.load(image_path, check_existing=True)
    else:
        bl_image = bpy.data.images.new(name=image_path, width=1, height=1)
        bl_image.generated_color = (0.0, 0.0, 0.0, 1.0)  # Default color if image not found
    # use suffix of image_path?
    bl_image.colorspace_settings.name = 'Linear Rec.709'  # Assuming the image is in Rec.709 color space
    node.image = bl_image
    # node.colorspace_settings.name = 'Linear Rec.709'
    node.interpolation = 'Linear'
    uv_map = create_blender_node(tree, mx_node, bpy.types.ShaderNodeUVMap)
    uv_tiling = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    uv_tiling.operation = 'MULTIPLY'
    uv_tiling.inputs[1].default_value = (1.0, 1.0, 1.0)  # Tiling factor
    uv_offset = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    uv_offset.operation = 'ADD'
    tree.links.new(node.inputs[0], uv_offset.outputs[0])  # Connect UV offset to image node
    tree.links.new(uv_tiling.inputs[0], uv_map.outputs[0])
    tree.links.new(uv_offset.inputs[0], uv_tiling.outputs[0])
    split_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeSeparateXYZ)
    tree.links.new(split_node.inputs[0], node.outputs[0]) # RGB to split
    mx_node_inputs = {}
    mx_node_inputs["texcoord"] = uv_tiling.inputs[0] # by default connected to uv_map node defined above
    mx_node_inputs["uvtiling"] = uv_tiling.inputs[1]
    mx_node_inputs["uvoffset"] = uv_offset.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": split_node.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_normalmap_float")
def ND_normalmap_float(tree: bpy.types.NodeTree, mx_node: mx.Node):
    # Blender's Normal Map node returns a world-space normal, which is what MaterialX's normalmap
    # outputs, so it connects directly. Any green-channel convention belongs to the image.
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeNormalMap)
    node.inputs[1].default_value = (0.5, 0.5, 1.0, 1.0)  # Default normal map value
    node.inputs[0].default_value = 1.0

    mx_node_inputs = {}
    mx_node_inputs["scale"] = node.inputs[0]
    mx_node_inputs["in"] = node.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_extract_color4")
def ND_extract_color4(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = blender_from_color4_bundle(tree, mx_node, bpy.types.ShaderNodeSeparateColor)
    constant = create_blender_node(tree, mx_node, bpy.types.NodeCombineBundle)
    constant.bundle_items.new("INT", "index")
    constant_out = create_blender_node(tree, mx_node, bpy.types.NodeSeparateBundle)
    constant_out.bundle_items.new("INT", "index")
    mix1 = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMix)
    mix2 = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMix)
    mix3 = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMix)
    mix4 = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMix)
    subtract2 = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    subtract2.operation = 'SUBTRACT'
    subtract2.use_clamp = True
    subtract2.inputs[1].default_value = 0.0
    subtract3 = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    subtract3.operation = 'SUBTRACT'
    subtract3.use_clamp = True
    subtract3.inputs[1].default_value = 1.0
    subtract4 = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMath)
    subtract4.operation = 'SUBTRACT'
    subtract4.use_clamp = True
    subtract4.inputs[1].default_value = 2.0
    tree.links.new(constant_out.inputs[0], constant.outputs[0])
    tree.links.new(mix1.inputs[2], node.outputs[0])
    tree.links.new(mix2.inputs[2], mix1.outputs[0])
    tree.links.new(mix2.inputs[3], node.outputs[1])
    tree.links.new(mix3.inputs[2], mix2.outputs[0])
    tree.links.new(mix3.inputs[3], node.outputs[2])
    tree.links.new(mix4.inputs[2], mix3.outputs[0])
    tree.links.new(mix4.inputs[3], node.outputs[3])
    tree.links.new(mix1.inputs[0], constant_out.outputs[0])
    tree.links.new(subtract2.inputs[0], constant_out.outputs[0])
    tree.links.new(subtract3.inputs[0], constant_out.outputs[0])
    tree.links.new(subtract4.inputs[0], constant_out.outputs[0])
    tree.links.new(mix2.inputs[0], subtract2.outputs[0])
    tree.links.new(mix3.inputs[0], subtract3.outputs[0])
    tree.links.new(mix4.inputs[0], subtract4.outputs[0])

    mx_node_inputs = {}
    mx_node_inputs["in"] = node.inputs[0]
    mx_node_inputs["index"] = constant.inputs[0]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": mix4.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_surfacematerial")
def ND_surfacematerial(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeOutputMaterial)
    mx_node_inputs = {}
    mx_node_inputs["surfaceshader"] = node.inputs[0]

    # apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_convert_color4_color3")
def ND_convert_color4_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    # if vector4 is an input, we have to also spawn an input of constants here
    vec4_input = blender_from_color4_bundle(tree, mx_node, bpy.types.NodeReroute)
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineColor)
    tree.links.new(vec4_input.outputs[0], node.inputs[0])
    tree.links.new(vec4_input.outputs[1], node.inputs[1])
    tree.links.new(vec4_input.outputs[2], node.inputs[2])

    mx_node_inputs = {}
    mx_node_inputs["in"] = vec4_input.inputs[0]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[0]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_multiply_color3")
def ND_multiply_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMix)
    node.data_type = 'RGBA'
    node.blend_type = 'MULTIPLY'
    node.update()
    node.inputs[0].default_value = 1.0  # Default factor for multiplication
    node.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)  # Default color for foreground
    node.inputs[7].default_value = (1.0, 1.0, 1.0, 1.0)  # Default color for background
    mx_node_inputs = {}
    mx_node_inputs["in1"] = node.inputs[6]
    mx_node_inputs["in2"] = node.inputs[7]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[2]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_mix_color3")
def ND_mix_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeMix)
    node.data_type = 'RGBA'
    node.blend_type = 'MIX'
    node.update()
    node.inputs[0].default_value = 0.0  # Default factor for mixing
    node.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)  # Default color for foreground
    node.inputs[7].default_value = (0.0, 0.0, 0.0, 1.0)  # Default color for background
    mx_node_inputs = {}
    mx_node_inputs["fg"] = node.inputs[6]
    mx_node_inputs["bg"] = node.inputs[7]
    mx_node_inputs["mix"] = node.inputs[0]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[2]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_convert_float_color3")
def ND_convert_float_color3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    combine_color = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineColor)
    combine_color.mode = 'HSV'
    combine_color.inputs[0].default_value = 0.0  # Default value for HSV
    combine_color.inputs[1].default_value = 0.0  # Default value for HSV
    combine_color.inputs[2].default_value = 0.0  # Default value for HSV

    mx_node_inputs = {}
    mx_node_inputs["in"] = combine_color.inputs[2]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": combine_color.outputs[0]}
    return (combine_color,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_distance_vector3")
def ND_distance_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeVectorMath)
    node.operation = 'DISTANCE'
    node.update()
    node.inputs[0].default_value = (0.0, 0.0, 0.0)  # Default vector value
    node.inputs[1].default_value = (0.0, 0.0, 0.0)  # Default vector value

    mx_node_inputs = {}
    mx_node_inputs["in1"] = node.inputs[0]
    mx_node_inputs["in2"] = node.inputs[1]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": node.outputs[1]}
    return (node,), mx_node_inputs, mx_node_outputs


@register_materialx_node("ND_convert_color3_vector3")
def ND_convert_color3_vector3(tree: bpy.types.NodeTree, mx_node: mx.Node):
    # if color3 is an input, we have to also spawn an input of constants here
    color_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeSeparateColor)
    color_node.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)  # Default color value
    vector_node = create_blender_node(tree, mx_node, bpy.types.ShaderNodeCombineXYZ)
    tree.links.new(vector_node.inputs[0], color_node.outputs[0])  # R
    tree.links.new(vector_node.inputs[1], color_node.outputs[1])  # G
    tree.links.new(vector_node.inputs[2], color_node.outputs[2])  # B

    mx_node_inputs = {}
    mx_node_inputs["in"] = color_node.inputs[0]

    apply_default_values(mx_node, mx_node_inputs)

    mx_node_outputs = {"out": vector_node.outputs[0]}
    return (color_node,), mx_node_inputs, mx_node_outputs
