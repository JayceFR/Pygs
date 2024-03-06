#version 330 

uniform sampler2D tex;
uniform sampler2D ui_tex;
uniform float time;

uniform sampler2D noise_tex1;
uniform float itime;

in vec2 uvs;
out vec4 f_color;

vec2 random2( vec2 p ) {
    return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
}

void overlay_frag(){
    f_color = vec4(texture(tex, uvs).rgb ,1.0);
    vec2 px_uvs = vec2(floor(uvs.x * 320) / 320, floor(uvs.y * 210) / 210);
    float center_dis = distance(uvs, vec2(0.5,0.5));
    float noise_val = center_dis + texture(noise_tex1, vec2(px_uvs.x * 1.52 * 2 + itime * 0.1, px_uvs.y * 2 - itime * 0.002)).r * 0.3;
    vec4 dark = vec4(0.0, 0.0, 0.0, 1.0);
    dark = vec4(0.0, 0.0, 0.0, 1.0);
    float darkness = max(0, noise_val - 0.7) * 10;
    float vignette = max(0, center_dis * center_dis - 0.1) * 5;
    darkness += center_dis;
    f_color = darkness * dark + (1 - darkness) * f_color;

    /*if ( noise_val > 0.85){
        f_color = vec4(0.1725, 0.0588, 0.2, 1.0);
    }
    else if (noise_val  > 0.8){
        f_color = vec4(0.4275, 0.502, 0.9804, 1.0);
    }*/

    vec4 ui_color = texture(ui_tex, uvs);
    if (ui_color.a > 0){
        f_color = ui_color;
    }
}

uniform vec2 scroll = vec2(0.1, 0.3);
uniform vec2 scroll2 = vec2(-0.13, 0.5);

void fire(){
    f_color = vec4(texture(tex, uvs).rgb, 1.0);
    vec2 fireCenter = vec2(0.9, 0.5); // Adjust the coordinates as needed

    // Convert UV coordinates to screen coordinates
    vec2 screenCoord = uvs * vec2(320.0, 210.0); // Assuming screen resolution is 320x210

    // Calculate the distance from the current fragment to the fire center along both x and y axes
    float distanceX = abs(screenCoord.x - fireCenter.x * 320.0);
    float distanceY = abs(screenCoord.y - fireCenter.y * 210.0);

    // Define the half-width and half-height of the square for the fire effect
    float halfWidth = 16.0; // Adjust the width as needed
    float halfHeight = 37.0; // Adjust the height as needed

    // Check if the current fragment is within the square bounds
    if (distanceX < halfWidth && distanceY < halfHeight) {
        vec2 px_uvs = vec2(floor(uvs.x * 320) / 320, floor(uvs.y * 210) / 210);
        float texColor1 = texture(noise_tex1, px_uvs + scroll * itime * 0.7).r;
        float texColor2 = texture(noise_tex1, px_uvs + scroll2 * itime * 0.3).r;
        float energy = texColor1 * texColor2 - (1 - uvs.y) * 0.35;
        // Define gradient colors
        vec4 color1 = vec4(texture(tex, uvs).rgb, 1.0); // Transparent
        vec4 color2 = vec4(0.05, 0.05, 0.05, 1.0); // Almost black
        vec4 color3 = vec4(0.6, 0.2, 0.0, 1.0); // Dark orange
        vec4 color4 = vec4(0.8, 0.4, 0.0, 1.0); // Dark yellow
        vec4 color5 = vec4(0.6, 0.2, 0.0, 1.0); // Dark orange
        vec4 color6 = vec4(0.0, 0.0, 0.0, 0.0); // Almost black

        // Define energy thresholds
        float threshold1 = 0.0;
        float threshold2 = 0.1;
        float threshold3 = 0.15;
        float threshold4 = 0.25;
        float threshold5 = 0.3;

        // Interpolate between colors based on energy level
        vec4 finalColor;
        if (energy < threshold1) {
            finalColor = color1;
        } else if (energy < threshold2) {
            finalColor = mix(color1, color2, smoothstep(threshold1, threshold2, energy));
        } else if (energy < threshold3) {
            finalColor = mix(color2, color3, smoothstep(threshold2, threshold3, energy));
        } else if (energy < threshold4) {
            finalColor = mix(color3, color4, smoothstep(threshold3, threshold4, energy));
        } else if (energy < threshold5) {
            finalColor = mix(color4, color5, smoothstep(threshold4, threshold5, energy));
        } else {
            f_color =color6 ;
        }

        f_color = finalColor;
    }
    vec4 ui_color = texture(ui_tex, uvs);
}


void main(){
    //fire();
    overlay_frag();
}