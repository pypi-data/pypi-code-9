def main():
    import os
    import sys
    os.chdir(os.path.dirname(__file__))
    print os.path.dirname(__file__)

    import glfw
    import time
    from engine import Engine

    # Initialize the library
    if not glfw.init():
        sys.exit()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Window Name", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Make the window's context current
    glfw.make_context_current(window)

    # Get window size
    width, height = glfw.get_framebuffer_size(window)

    # Create engine
    engine = Engine(window)
    engine.setWindowHeight(height)
    engine.setWindowWidth(width)

    def on_resize(window, width, height):
        engine.setWindowWidth(width)
        engine.setWindowHeight(height)

    # Install a window size handler
    glfw.set_window_size_callback(window, on_resize)

    def on_key(window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, 1)

    # Install a key handler
    glfw.set_key_callback(window, on_key)

    def on_mouse(window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_1 and action == glfw.PRESS:
            engine.shoot_on()
        if button == glfw.MOUSE_BUTTON_1 and action == glfw.RELEASE:
            engine.shoot_off()
        if button == glfw.MOUSE_BUTTON_2 and action == glfw.PRESS:
            engine.camera_switch()

    glfw.set_mouse_button_callback(window, on_mouse)

    def on_scroll(window, x, y):
        engine.camera_scroll(y)

    glfw.set_scroll_callback(window, on_scroll)

    old_time = time.time()
    elapsed_time = 0.0

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Calculate elapsed time
        elapsed_time = time.time() - old_time
        old_time = time.time()

        # Process
        engine.step(elapsed_time)

        # Swap front and back buffers
        glfw.swap_interval(1)
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

        # Don't be egoist :)
        time.sleep(0.01)

    glfw.terminate()


if __name__ == '__main__':
    main()
