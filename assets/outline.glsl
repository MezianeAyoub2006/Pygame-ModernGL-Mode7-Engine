#version 330
in vec2 uv;
out vec4 fragColor;
uniform sampler2D tex;

void main() {
    float d = 0.003;
    vec4 c = texture(tex, uv);
    
    float a = 0.0;
    a += texture(tex, uv + vec2( d,  0)).a;
    a += texture(tex, uv + vec2(-d,  0)).a;
    a += texture(tex, uv + vec2( 0,  d)).a;
    a += texture(tex, uv + vec2( 0, -d)).a;
    
    vec4 outline_color = vec4(0.0, 0.0, 0.0, 1.0);
    
    if (c.a < 0.5 && a > 0.0)
        fragColor = outline_color;
    else
        fragColor = c;
}