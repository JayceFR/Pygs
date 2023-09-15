import pygame
class Hud():
    def __init__(self) -> None:
        pygame.init()
        self.joysticks = {}
        self.return_dict = {"run" : True, "left" : False, "right" : False, "jump": False, "x_axis" : 0.0}

    def events(self):
        # self.return_dict = {"run" : True, "left" : False, "right" : False, "jump": False}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.return_dict["run"] = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    joystick = self.joysticks[event.instance_id]
                    self.return_dict["jump"] = True
                    # if joystick.rumble(0, 0.7, 500):
                    #     print(f"Rumble effect played on joystick {event.instance_id}")
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    self.return_dict["jump"] = False
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    self.return_dict["x_axis"] = event.value
            if event.type == pygame.JOYDEVICEADDED:
                print(event)
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                print(str(joy.get_instance_id()) + " Connected ")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.return_dict["right"] = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.return_dict["left"] = True
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.return_dict["jump"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.return_dict["right"] = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.return_dict["left"] = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.return_dict["jump"] = False
    
    def get_controls(self):
        return self.return_dict