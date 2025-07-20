from phue import Bridge, PhueRequestTimeout, PhueRegistrationException

class Lights:
    """
    Manages Hue lights that are connected to a Hue Bridge.
    """

    def __init__(self):
        self._bridge_ip = None
        self._bridge = None
        self._controlled_lights = []
    
    
    def connect(self, new_bridge_ip: str | None = None) -> bool:
        """
        Connects to the Hue Bridge using it's IP address.

        Args:
            new_bridge_ip (str | None, optional): The IP address of the Hue Bridge. Defaults to None.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Checking for new bridge ip
            if new_bridge_ip is not None:
                self.bridge_ip = new_bridge_ip 
            # Checking if _bridge_ip has not been set
            if self._bridge_ip is None:
                print("Error: Bridge IP is needed to connect.")
                return False
            # Connecting to the bridge
            self._bridge = Bridge(self._bridge_ip) 
            return True
        except PhueRequestTimeout:
            print(f"Error: Bridge at {self._bridge_ip} not found or is not reachable.")
            return False
        except PhueRegistrationException:
            print("Error: Press the button on the bridge to register.")
            return False
        except ValueError as e:
            print(e)
            return False

    @property
    def bridge_ip(self) -> str:
        """
        Returns the IP address of the Hue Bridge
        """
        return self._bridge_ip
    
    @bridge_ip.setter
    def bridge_ip(self, bridge_ip: str) -> None:
        """
        Sets the IP address for the Hue Bridge.

        Args:
            bridge_ip (str): The IP address.

        Raises:
            ValueError: If bridge_ip is not an str.
        """
        if not isinstance(bridge_ip, str):
            raise ValueError("Error: bridge_ip must be a string.")
        self._bridge_ip = bridge_ip

    @property
    def controlled_lights(self) -> str:
        """
        Returns the names of the controlled lights.
        """
        return self._controlled_lights
    
    @controlled_lights.setter
    def controlled_lights(self, controlled_lights: list):
        """
        Sets the list of controlled light names.

        Args:
            controlled_lights (list): A list of light names to be controlled.
        """
        self._controlled_lights = controlled_lights
      
    def add_light(self, light_name: str) -> bool:
        """
        Adds a light name to _controlled_lights.

        Args:
            light_name (str): The name of the light.

        Returns:
            bool: True if successful, False otherwise.
        """
        # Checking if connected to the bridge
        if self._bridge is None:
            print("Error: Not connected to the bridge.")
            return False
        # Checking if the light is not connected to the bridge
        if light_name not in self._bridge.get_light_objects('name'):
            print(f"Error: Light \"{light_name}\" is not connected to the bridge.")
            return False
        # Checking if the light is controlled
        if light_name in self._controlled_lights:
            print(f"Error: Light \"{light_name}\" has already been added.")
            return False
        # Adding the light to _controlled_lights
        self._controlled_lights.append(light_name)
        print(f"Light \"{light_name}\" has been added.")
        return True

    def remove_light(self, light_name: str) -> bool:
        """
        Removes a light name from _controlled_lights.

        Args:
            light_name (str): The name of the light.

        Returns:
            bool: True if successful, False otherwise.
        """
        # Checking if connected to the bridge
        if self._bridge is None:
            print("Error: Not connected to the bridge.")
            return False
        # Checking if the light is not connected to the bridge
        if light_name not in self._bridge.get_light_objects('name'):
            print(f"Error: Light \"{light_name}\" is not connected to the bridge.")
            return False
        # Checking if the light is not being controlled
        if light_name not in self._controlled_lights:
            print(f"Error: Light \"{light_name}\" was not a controlled light.") 
            return False
        # Removing the light from the controlled lights
        self._controlled_lights.remove(light_name)
        print(f"Light \"{light_name}\" has been removed.")
        return True
    
    def turn_on(self) -> bool: 
        """
        Turns on all controlled lights.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self._bridge is None:
            print("Error: Not connected to the bridge.")
            return False
        # Getting all lights connected to the bridge
        lights = self._bridge.get_light_objects('name')
        # Turning on each of the controlled lights
        for light_name in self._controlled_lights:
            lights[light_name].on = True
        return True
        
    def turn_off(self) -> bool: 
        """
        Turns off all controlled lights.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self._bridge is None:
            print("Error: Not connected to the bridge.")
            return False
        # Getting all lights connected to the bridge
        lights = self._bridge.get_light_objects('name')
        # Turning off each of the controlled lights 
        for light_name in self._controlled_lights:
            lights[light_name].on = False
        return True