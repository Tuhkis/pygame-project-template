#version 330 core

uniform vec2 particlePos;

in vec2 vert;
in vec2 texCoord;

out vec2 uvs;

void main() {
	uvs = texCoord;
	vec2 v = vert + particlePos;
	v.x /= 512;
	v.y /= -300;
	v -= vec2(1.0f, -1.0f);
	gl_Position = vec4(v, 0.0f, 1.0f);
}

