//
//  main.cpp
//  OpenGL Schrodinger
//
//  Created by Liam Clink on 2/7/18.
//
//

// OpenGL practice
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <iostream>

#include <GL/glew.h> // include GLEW and new version of GL on Windows
#include <GLFW/glfw3.h> // GLFW helper library
#include <stdio.h>

struct vertex
{
    GLfloat x, y;
    
    void set_vertex(double x_new, double y_new)
    {
        x = x_new;
        y = y_new;
    }
};

void circle(vertex *vertices, int segments, float x, float y, float r)
{
    vertices[0].set_vertex(x, y);
    
    for( int n = 0; n <= segments; ++n ) {
        float const t = 2 * M_PI * (float)n / (float)segments;
        vertices[n+1].set_vertex(x + r*sin(t), y + r*cos(t));
    }

}

void check_GLSL_compile(GLuint shader)
{
    // Check GLSL compile status
    GLint status = 0; glGetShaderiv(shader, GL_COMPILE_STATUS, &status);
    std::cout << "Compile status: " << status << std::endl;
    
    if (!status)
    {
        // Print GLSL compile log
        GLint logLen = 0; glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &logLen);
        GLchar* logStr = new GLchar[logLen];
        glGetShaderInfoLog(shader, logLen, 0, logStr); // report logStr delete[] logStr;
        std::cout << "Compile logStr: " << logStr << std::endl;
    }
}

void check_GLSL_link(GLuint shader_program)
{
    // Check GLSL compile status
    GLint status = 0; glGetProgramiv(shader_program, GL_LINK_STATUS, &status);
    std::cout << "Link status: " << status << std::endl;
    
    if (!status)
    {
        // Print GLSL compile log
        GLint logLen = 0; glGetProgramiv(shader_program, GL_INFO_LOG_LENGTH, &logLen);
        GLchar* logStr = new GLchar[logLen];
        glGetShaderInfoLog(shader_program, logLen, 0, logStr); // report logStr delete[] logStr;
        std::cout << "Link logStr: " << logStr << std::endl;
    }
}

int main() {
    // start GL context and O/S window using the GLFW helper library
    if (!glfwInit()) {
        fprintf(stderr, "ERROR: could not start GLFW3\n");
        return 1;
    }
    
    // uncomment these lines if on Apple OS X
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    
    GLFWwindow* window = glfwCreateWindow(640, 480, "Hello Triangle", NULL, NULL);
    if (!window)
        fprintf(stderr, "ERROR: could not open window with GLFW3\n");
    
    glfwMakeContextCurrent(window);
    
    // start GLEW extension handler
    glewExperimental = GL_TRUE;
    // Initialize GLEW, must be done after window creation
    GLenum err = glewInit();
    if (GLEW_OK != err)
    {
        /* Problem: glewInit failed, something is seriously wrong. */
        fprintf(stderr, "Error: %s\n", glewGetErrorString(err));
    }
    fprintf(stdout, "Status: Using GLEW %s\n", glewGetString(GLEW_VERSION));
    
    // get version info
    const GLubyte* renderer = glGetString(GL_RENDERER); // get renderer string
    const GLubyte* version = glGetString(GL_VERSION); // version as a string
    printf("Renderer: %s\n", renderer);
    printf("OpenGL version supported %s\n", version);
    
    float points[] = {
        0.0f,  0.5f,  0.0f,
        0.5f, -0.5f,  0.0f,
        -0.5f, -0.5f,  0.0f
    };
    
    float colours[] = {
        1.0f, 0.0f,  0.0f,
        0.0f, 1.0f,  0.0f,
        0.0f, 0.0f,  1.0f
    };
    
    
    //Initialize vertex buffer object
    GLuint points_vbo = 0;
    glGenBuffers(1, &points_vbo);
    glBindBuffer(GL_ARRAY_BUFFER, points_vbo);
    glBufferData(GL_ARRAY_BUFFER, 9 * sizeof(float), points, GL_STATIC_DRAW);
    
    GLuint colours_vbo = 0;
    glGenBuffers(1, &colours_vbo);
    glBindBuffer(GL_ARRAY_BUFFER, colours_vbo);
    glBufferData(GL_ARRAY_BUFFER, 9 * sizeof(float), colours, GL_STATIC_DRAW);
    
    GLuint vao = 0;
    glGenVertexArrays(1, &vao);
    glBindVertexArray(vao);
    glBindBuffer(GL_ARRAY_BUFFER, points_vbo);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, NULL);
    glBindBuffer(GL_ARRAY_BUFFER, colours_vbo);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, NULL);
    
    glEnableVertexAttribArray(0);
    glEnableVertexAttribArray(1);
    
    //Define vertex shader (better to load from text file)
    const char* vertex_shader =
    "#version 400\n"
    "in vec3 vertex_position;"
    "in vec3 vertex_color;"
    "out vec3 color;"
    "void main() {"
    "  color = vertex_color;"
    "  gl_Position = vec4(vertex_position, 1.0);"
    "}";
    
    //Define fragment shader (for drawing surfaces)
    const char* fragment_shader =
    "#version 400\n"
    "in vec3 color;"
    "out vec4 frag_color;"
    "void main() {"
    "  frag_color = vec4(color, 1.0);"
    "}";
    
    
    //Compile shaders
    GLuint vs = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vs, 1, &vertex_shader, NULL);
    glCompileShader(vs);
    
    GLuint fs = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fs, 1, &fragment_shader, NULL);
    glCompileShader(fs);
    
    
    //Link shaders into program
    GLuint shader_program = glCreateProgram();
    glAttachShader(shader_program, vs);
    glAttachShader(shader_program, fs);
    
    // insert location binding code here
    glBindAttribLocation(shader_program, 0, "vertex_position");
    glBindAttribLocation(shader_program, 1, "vertex_color");
    
    glLinkProgram(shader_program);
    
    //Draw in a loop
    while(!glfwWindowShouldClose(window)) {
        // wipe the drawing surface clear
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        
        //---Render OpenGL stuff---//
        glUseProgram(shader_program);
        
        glBindVertexArray(vao);
        // draw points 0-3 from the currently bound VAO with current in-use shader
        glDrawArrays(GL_TRIANGLES, 0, 3);
        
        // update other events like input handling
        glfwPollEvents();
        
        // put the stuff we've been drawing onto the display
        glfwSwapBuffers(window);
        
        if(glfwGetKey(window, GLFW_KEY_ESCAPE)) {
            glfwSetWindowShouldClose(window, 1);
        }
    }
    
    glfwTerminate();
    return 0;
}
