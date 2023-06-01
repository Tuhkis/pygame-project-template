#version 330 core

uniform sampler2D tex;
uniform vec3 colour;

in vec2 uvs;

out vec4 f_color;

void main() {
	vec4 t = texture(tex, uvs);
	f_color = vec4(t.rgb * colour, t.r);
	// f_color = vec4(uvs.xy, 0.0f, 1.0f);
}

