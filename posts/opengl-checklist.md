---
title: 'OpenGL Checklist'
subtitle: "A list of things to check if your GL code isn't working."
date: '2019-09-25'
author: 'Aleksander B. Birkeland'
---

#### Amazing OpenGL documentation
[docs.gl](http://docs.gl/)

#### RenderDoc
RenderDoc may not always work perfectly but it is very nice to be able inspect
your buffers to make sure stride, etc. is set correctly. 
[OpenGL version support](https://renderdoc.org/docs/behind_scenes/opengl_support.html)

**Website:** [RenderDoc](https://renderdoc.org/)

**Other debuggers:**

- [NVIDIA Nsight](http://www.nvidia.com/object/nsight.html) - IDE plugin
- [NVIDIA Nsight Graphics](https://developer.nvidia.com/nsight-graphics) - Standalone debugger
- [Even more debuggers](https://github.com/eug/awesome-opengl#debug)

#### Do you use 4.3+? Enable debug messages!
[Enabling debug messages](#enabling-debug-messages)

#### Are you on 3.3+
- Remeber to bind a vertex array [glBindVertexArray](http://docs.gl/gl4/glBindVertexArray)

#### Basic checklist
- Did you set the correct context version and profile?
- Did you enable debug messages? [Enabling debug messages](#enabling-debug-messages)
- Is the shader bound? [glUseProgram](http://docs.gl/gl4/glUseProgram)
- Did the shader actually link? [glGetProgramiv](http://docs.gl/gl4/glGetProgram)
- Did you bind all the buffers? [glBindBuffer](http://docs.gl/gl4/glBindBuffer)
- Did you enable all the vertex attribs? [glEnableVertexAttribArray](http://docs.gl/gl4/glEnableVertexAttribArray)

#### Enabling debug messages

```c++
const char* source_to_string(GLenum source) {
    switch (source) {
        case GL_DEBUG_SOURCE_API:
            return "GL_DEBUG_SOURCE_API";
        case GL_DEBUG_SOURCE_WINDOW_SYSTEM:
            return "GL_DEBUG_SOURCE_WINDOW_SYSTEM";
        case GL_DEBUG_SOURCE_SHADER_COMPILER:
            return "GL_DEBUG_SOURCE_SHADER_COMPILER";
        case GL_DEBUG_SOURCE_THIRD_PARTY:
            return "GL_DEBUG_SOURCE_THIRD_PARTY";
        case GL_DEBUG_SOURCE_APPLICATION:
            return "GL_DEBUG_SOURCE_APPLICATION";
        case GL_DEBUG_SOURCE_OTHER:
            return "GL_DEBUG_SOURCE_OTHER";
        default:
            return "INVALID_SOURCE";
    }
}

const char* type_to_string(GLenum type) {
    switch (type) {
        case GL_DEBUG_TYPE_ERROR:
            return "GL_DEBUG_TYPE_ERROR";
        case GL_DEBUG_TYPE_DEPRECATED_BEHAVIOR:
            return "GL_DEBUG_TYPE_DEPRECATED_BEHAVIOR";
        case GL_DEBUG_TYPE_UNDEFINED_BEHAVIOR:
            return "GL_DEBUG_TYPE_UNDEFINED_BEHAVIOR";
        case GL_DEBUG_TYPE_PORTABILITY:
            return "GL_DEBUG_TYPE_PORTABILITY";
        case GL_DEBUG_TYPE_PERFORMANCE:
            return "GL_DEBUG_TYPE_PERFORMANCE";
        case GL_DEBUG_TYPE_MARKER:
            return "GL_DEBUG_TYPE_MARKER";
        case GL_DEBUG_TYPE_PUSH_GROUP:
            return "GL_DEBUG_TYPE_PUSH_GROUP";
        case GL_DEBUG_TYPE_POP_GROUP:
            return "GL_DEBUG_TYPE_POP_GROUP";
        case GL_DEBUG_TYPE_OTHER:
            return "GL_DEBUG_TYPE_OTHER";
        default:
            return "INVALID_TYPE";
    }
}

const char* severity_to_string(GLenum severity) {
    switch (severity) {
        case GL_DEBUG_SEVERITY_LOW:
            return "GL_DEBUG_SEVERITY_LOW";
        case GL_DEBUG_SEVERITY_MEDIUM:
            return "GL_DEBUG_SEVERITY_MEDIUM";
        case GL_DEBUG_SEVERITY_HIGH:
            return "GL_DEBUG_SEVERITY_HIGH";
        case GL_DEBUG_SEVERITY_NOTIFICATION:
            return "GL_DEBUG_SEVERITY_NOTIFICATION";
        default:
            return "INVALID_SEVERITY";
    }
}

void gl_log_func(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam) {
    fprintf(stdout, "source: %s, type: %s, id: %u, severity: %s, msg: %s\n",
            source_to_string(source),
            type_to_string(type),
            id,
            severity_to_string(severity),
            message);
    fflush(stdout);
}

...
	glEnable(GL_DEBUG_OUTPUT);
	glDebugMessageCallback(gl_log_func, 0);
	// Optional. Less spam from drivers
	glDebugMessageControl( GL_DONT_CARE, GL_DONT_CARE, GL_DEBUG_SEVERITY_NOTIFICATION, 0, 0, GL_FALSE);
...
```