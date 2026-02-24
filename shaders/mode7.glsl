#version 330 core

in vec2 uv;
out vec4 fragColor;
uniform sampler2D tex;
uniform sampler2D tex_infinite;
uniform float tex_infinite_scale;

uniform float player_x;
uniform float player_y;
uniform float player_z;
uniform float player_angle;
uniform float horizon_height;
uniform float time;

void main() {
    float screenY = 1.0 - uv.y;

    if (screenY < horizon_height) {
        fragColor = vec4(0.4, 0.7, 1.0, 1.0);
        return;
    }

    float depth = screenY - horizon_height;
    if (depth < 0.002) {
        fragColor = vec4(0.4, 0.7, 1.0, 1.0);
        return;
    }

    float z = min(1.0 / depth, 300.0);
    float centeredX = uv.x - 0.5;

    float scale = player_z * player_z / 100.0;

    float xi = centeredX * z * scale + player_x;
    float yi = z * scale + player_y;

    float A = cos(player_angle);
    float B = -sin(player_angle);
    float C = sin(player_angle);
    float D = cos(player_angle);

    float xi2 = xi - player_x;
    float yi2 = yi - player_y;

    vec2 pixel = vec2(
        A * xi2 + B * yi2 + player_x,
        C * xi2 + D * yi2 + player_y
    );



    vec4 color;
    if (pixel.x < 0.0 || pixel.x > 1.0 || pixel.y < 0.0 || pixel.y > 1.0) {
        color = texture(tex_infinite, fract(pixel * tex_infinite_scale));
    } else {
        color = texture(tex, pixel);
    }

    
    vec4 fog_color = vec4(0.4, 0.7, 1.0, 1.0);  
    float fog_start = 20.0;   
    float fog_end   = 100.0;  
    float fog_factor = clamp((z - fog_start) / (fog_end - fog_start), 0.0, 1.0);
    
    fragColor = mix(color, fog_color, fog_factor);
}