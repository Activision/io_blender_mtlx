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


@register_materialx_node("ND_open_pbr_surface_surfaceshader")
def ND_open_pbr_surface_surfaceshader(tree: bpy.types.NodeTree, mx_node: mx.Node):
    ShaderNodeBsdfPrincipled_2 = create_blender_node(tree, mx_node, 'ShaderNodeBsdfPrincipled')
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Base Color'].default_value = (0.6000000238418579, 0.6000000238418579, 0.6000000238418579, 1.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Metallic'].default_value = 1.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Roughness'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['IOR'].default_value = 1.5
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Alpha'].default_value = 1.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Normal'].default_value = (0.0, 0.0, 0.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Diffuse Roughness'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Subsurface Weight'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Subsurface Radius'].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Subsurface Scale'].default_value = 0.05000000074505806
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Subsurface Anisotropy'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Specular IOR Level'].default_value = 0.5
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Specular Tint'].default_value = (1.0, 0.0, 0.007685747928917408, 1.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Anisotropic'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Anisotropic Rotation'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Tangent'].default_value = (0.0, 0.0, 0.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Transmission Weight'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Coat Weight'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Coat Roughness'].default_value = 0.029999999329447746
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Coat IOR'].default_value = 1.5
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Coat Tint'].default_value = (1.0, 1.0, 1.0, 1.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Coat Normal'].default_value = (0.0, 0.0, 0.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Sheen Weight'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Sheen Roughness'].default_value = 0.5
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Sheen Tint'].default_value = (1.0, 1.0, 1.0, 1.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Emission Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Emission Strength'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Thin Film Thickness'].default_value = 0.0
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeBsdfPrincipled_2.inputs['Thin Film IOR'].default_value = 1.3300000429153442
    ShaderNodeBsdfPrincipled_2.update()
    ShaderNodeMix_3 = create_blender_node(tree, mx_node, 'ShaderNodeMix')
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.data_type = 'RGBA'
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.blend_type = 'MULTIPLY'
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.inputs[0].default_value = 1.0
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.inputs[6].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_3.update()
    ShaderNodeMix_3.inputs[7].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_3.update()
    ShaderNodeCombineColor_4 = create_blender_node(tree, mx_node, 'ShaderNodeCombineColor')
    ShaderNodeCombineColor_4.update()
    ShaderNodeCombineColor_4.mode = 'HSV'
    ShaderNodeCombineColor_4.update()
    ShaderNodeCombineColor_4.inputs[0].default_value = 0.0
    ShaderNodeCombineColor_4.update()
    ShaderNodeCombineColor_4.inputs[1].default_value = 0.0
    ShaderNodeCombineColor_4.update()
    ShaderNodeCombineColor_4.inputs[2].default_value = 1.0
    ShaderNodeCombineColor_4.update()
    ShaderNodeMix_5 = create_blender_node(tree, mx_node, 'ShaderNodeMix')
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.data_type = 'RGBA'
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.blend_type = 'MULTIPLY'
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.inputs[0].default_value = 1.0
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.inputs[6].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_5.update()
    ShaderNodeMix_5.inputs[7].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_5.update()
    ShaderNodeCombineColor_6 = create_blender_node(tree, mx_node, 'ShaderNodeCombineColor')
    ShaderNodeCombineColor_6.update()
    ShaderNodeCombineColor_6.mode = 'HSV'
    ShaderNodeCombineColor_6.update()
    ShaderNodeCombineColor_6.inputs[0].default_value = 0.0
    ShaderNodeCombineColor_6.update()
    ShaderNodeCombineColor_6.inputs[1].default_value = 0.0
    ShaderNodeCombineColor_6.update()
    ShaderNodeCombineColor_6.inputs[2].default_value = 1.0
    ShaderNodeCombineColor_6.update()
    ShaderNodeCombineXYZ_7 = create_blender_node(tree, mx_node, 'ShaderNodeCombineXYZ')
    ShaderNodeCombineXYZ_7.update()
    ShaderNodeCombineXYZ_7.inputs[0].default_value = 0.0
    ShaderNodeCombineXYZ_7.update()
    ShaderNodeCombineXYZ_7.inputs[1].default_value = 0.0
    ShaderNodeCombineXYZ_7.update()
    ShaderNodeCombineXYZ_7.inputs[2].default_value = 0.0
    ShaderNodeCombineXYZ_7.update()
    ShaderNodeSeparateColor_8 = create_blender_node(tree, mx_node, 'ShaderNodeSeparateColor')
    ShaderNodeSeparateColor_8.update()
    ShaderNodeSeparateColor_8.mode = 'RGB'
    ShaderNodeSeparateColor_8.update()
    ShaderNodeSeparateColor_8.inputs[0].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    ShaderNodeSeparateColor_8.update()
    ShaderNodeMix_9 = create_blender_node(tree, mx_node, 'ShaderNodeMix')
    ShaderNodeMix_9.update()
    ShaderNodeMix_9.data_type = 'RGBA'
    ShaderNodeMix_9.update()
    ShaderNodeMix_9.blend_type = 'MULTIPLY'
    ShaderNodeMix_9.update()
    ShaderNodeMix_9.inputs[0].default_value = 1.0
    ShaderNodeMix_9.update()
    ShaderNodeMix_9.inputs[6].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_9.update()
    ShaderNodeMix_9.inputs[7].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_9.update()
    ShaderNodeCombineColor_10 = create_blender_node(tree, mx_node, 'ShaderNodeCombineColor')
    ShaderNodeCombineColor_10.update()
    ShaderNodeCombineColor_10.mode = 'HSV'
    ShaderNodeCombineColor_10.update()
    ShaderNodeCombineColor_10.inputs[0].default_value = 0.0
    ShaderNodeCombineColor_10.update()
    ShaderNodeCombineColor_10.inputs[1].default_value = 0.0
    ShaderNodeCombineColor_10.update()
    ShaderNodeCombineColor_10.inputs[2].default_value = 1.0
    ShaderNodeCombineColor_10.update()
    ShaderNodeMix_11 = create_blender_node(tree, mx_node, 'ShaderNodeMix')
    ShaderNodeMix_11.update()
    ShaderNodeMix_11.data_type = 'RGBA'
    ShaderNodeMix_11.update()
    ShaderNodeMix_11.blend_type = 'MULTIPLY'
    ShaderNodeMix_11.update()
    ShaderNodeMix_11.inputs[0].default_value = 1.0
    ShaderNodeMix_11.update()
    ShaderNodeMix_11.inputs[6].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_11.update()
    ShaderNodeMix_11.inputs[7].default_value = (0.5, 0.5, 0.5, 1.0)
    ShaderNodeMix_11.update()
    ShaderNodeMath_12 = create_blender_node(tree, mx_node, 'ShaderNodeMath')
    ShaderNodeMath_12.update()
    ShaderNodeMath_12.inputs[0].default_value = 0.5
    ShaderNodeMath_12.update()
    ShaderNodeMath_12.inputs[1].default_value = 0.5
    ShaderNodeMath_12.update()
    mx_node_inputs = {}
    mx_node_outputs = {}
    tree.links.new(ShaderNodeMix_3.outputs[2], ShaderNodeBsdfPrincipled_2.inputs['Base Color'])
    mx_node_outputs['out'] = ShaderNodeBsdfPrincipled_2.outputs[0]
    tree.links.new(ShaderNodeCombineColor_4.outputs[0], ShaderNodeMix_3.inputs[6])
    mx_node_inputs['base_weight'] = ShaderNodeCombineColor_4.inputs[2]
    mx_node_inputs['base_color'] = ShaderNodeMix_3.inputs[7]
    mx_node_inputs['base_diffuse_roughness'] = ShaderNodeBsdfPrincipled_2.inputs['Diffuse Roughness']
    mx_node_inputs['base_metalness'] = ShaderNodeBsdfPrincipled_2.inputs['Metallic']
    tree.links.new(ShaderNodeCombineColor_6.outputs[0], ShaderNodeMix_5.inputs[6])
    tree.links.new(ShaderNodeMix_5.outputs[2], ShaderNodeBsdfPrincipled_2.inputs['Specular Tint'])
    mx_node_inputs['specular_weight'] = ShaderNodeCombineColor_6.inputs[2]
    mx_node_inputs['specular_color'] = ShaderNodeMix_5.inputs[7]
    mx_node_inputs['specular_roughness'] = ShaderNodeBsdfPrincipled_2.inputs['Roughness']
    mx_node_inputs['specular_ior'] = ShaderNodeBsdfPrincipled_2.inputs['IOR']
    mx_node_inputs['specular_roughness_anisotropy'] = ShaderNodeBsdfPrincipled_2.inputs['Anisotropic']
    mx_node_inputs['transmission_weight'] = ShaderNodeBsdfPrincipled_2.inputs['Transmission Weight']
    mx_node_inputs['subsurface_weight'] = ShaderNodeBsdfPrincipled_2.inputs['Subsurface Weight']
    tree.links.new(ShaderNodeSeparateColor_8.outputs[0], ShaderNodeCombineXYZ_7.inputs[0])
    tree.links.new(ShaderNodeSeparateColor_8.outputs[1], ShaderNodeCombineXYZ_7.inputs[1])
    tree.links.new(ShaderNodeSeparateColor_8.outputs[2], ShaderNodeCombineXYZ_7.inputs[2])
    mx_node_inputs['subsurface_radius'] = ShaderNodeBsdfPrincipled_2.inputs['Subsurface Scale']
    mx_node_inputs['subsurface_color'] = ShaderNodeMix_9.inputs[6]
    mx_node_inputs['subsurface_radius_scale'] = ShaderNodeMix_9.inputs[7]
    tree.links.new(ShaderNodeMix_9.outputs[2], ShaderNodeSeparateColor_8.inputs[0])
    tree.links.new(ShaderNodeCombineXYZ_7.outputs[0], ShaderNodeBsdfPrincipled_2.inputs['Subsurface Radius'])
    mx_node_inputs['subsurface_scatter_anisotropy'] = ShaderNodeBsdfPrincipled_2.inputs['Subsurface Anisotropy']
    mx_node_inputs['fuzz_weight'] = ShaderNodeBsdfPrincipled_2.inputs['Sheen Weight']
    mx_node_inputs['fuzz_color'] = ShaderNodeBsdfPrincipled_2.inputs['Sheen Tint']
    mx_node_inputs['fuzz_roughness'] = ShaderNodeBsdfPrincipled_2.inputs['Sheen Roughness']
    mx_node_inputs['coat_weight'] = ShaderNodeBsdfPrincipled_2.inputs['Coat Weight']
    mx_node_inputs['coat_roughness'] = ShaderNodeBsdfPrincipled_2.inputs['Coat Roughness']
    mx_node_inputs['coat_ior'] = ShaderNodeBsdfPrincipled_2.inputs['Coat IOR']
    mx_node_inputs['coat_darkening'] = ShaderNodeCombineColor_10.inputs[2]
    mx_node_inputs['coat_color'] = ShaderNodeMix_11.inputs[6]
    tree.links.new(ShaderNodeCombineColor_10.outputs[0], ShaderNodeMix_11.inputs[7])
    tree.links.new(ShaderNodeMix_11.outputs[2], ShaderNodeBsdfPrincipled_2.inputs['Coat Tint'])
    mx_node_inputs['thin_film_ior'] = ShaderNodeBsdfPrincipled_2.inputs['Thin Film IOR']
    mx_node_inputs['thin_film_thickness'] = ShaderNodeMath_12.inputs[1]
    tree.links.new(ShaderNodeMath_12.outputs[0], ShaderNodeBsdfPrincipled_2.inputs['Thin Film Thickness'])
    mx_node_inputs['thin_film_weight'] = ShaderNodeMath_12.inputs[0]
    mx_node_inputs['emission_luminance'] = ShaderNodeBsdfPrincipled_2.inputs['Emission Strength']
    mx_node_inputs['emission_color'] = ShaderNodeBsdfPrincipled_2.inputs['Emission Color']
    mx_node_inputs['geometry_opacity'] = ShaderNodeBsdfPrincipled_2.inputs['Alpha']
    mx_node_inputs['geometry_normal'] = ShaderNodeBsdfPrincipled_2.inputs['Normal']
    mx_node_inputs['geometry_coat_normal'] = ShaderNodeBsdfPrincipled_2.inputs['Coat Normal']
    mx_node_inputs['geometry_tangent'] = ShaderNodeBsdfPrincipled_2.inputs['Tangent']
    apply_default_values(mx_node, mx_node_inputs)
    return (ShaderNodeBsdfPrincipled_2,ShaderNodeMix_3,ShaderNodeCombineColor_4,ShaderNodeMix_5,ShaderNodeCombineColor_6,ShaderNodeCombineXYZ_7,ShaderNodeSeparateColor_8,ShaderNodeMix_9,ShaderNodeCombineColor_10,ShaderNodeMix_11,ShaderNodeMath_12), mx_node_inputs, mx_node_outputs
