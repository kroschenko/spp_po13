from abc import ABC 
 
 
class TV(ABC): 
    def __init__(self): 
        self.power = False 
        self.volume = 10 
        self.channel = 1 
 
    def turn_on(self): 
        self.power = True 
        print("TV is ON") 
 
    def turn_off(self): 
        self.power = False 
        print("TV is OFF") 
 
    def volume_up(self): 
        if self.volume < 100: 
            self.volume += 1 
        print(f"Volume: {self.volume}") 
 
    def volume_down(self): 
        if self.volume > 0: 
            self.volume -= 1 
        print(f"Volume: {self.volume}") 
 
    def channel_up(self): 
        self.channel += 1 
        if self.channel > 999: 
            self.channel = 1 
        print(f"Channel: {self.channel}") 
 
    def channel_down(self): 
        self.channel -= 1 
        if self.channel < 1: 
            self.channel = 999 
        print(f"Channel: {self.channel}") 
 
 
class SonyTV(TV): 
    def __init__(self): 
        super().__init__() 
        print("Sony TV created") 
 
 
class SamsungTV(TV): 
    def __init__(self): 
        super().__init__() 
        print("Samsung TV created") 
 
 
class RemoteControl: 
    def __init__(self, tv): 
        self.tv = tv 
 
    def toggle_power(self): 
        if self.tv.power: 
            self.tv.turn_off() 
        else: 
            self.tv.turn_on() 
 
    def volume_up(self): 
        self.tv.volume_up() 
 
    def volume_down(self): 
        self.tv.volume_down() 
 
    def channel_up(self): 
        self.tv.channel_up() 
 
    def channel_down(self): 
        self.tv.channel_down() 
 
 
class BasicRemote(RemoteControl): 
    def mute(self): 
        self.tv.volume = 0 
        print("Muted") 
 
 
class AdvancedRemote(RemoteControl): 
    def set_channel(self, number): 
        if 1 <= number <= 999: 
            self.tv.channel = number 
            print(f"Channel set to {number}") 
        else: 
            print("Invalid channel number") 
def main(): 
print("Bridge pattern demo\n") 
tv = SonyTV() 
print() 
remote = BasicRemote(tv) 
remote.toggle_power() 
remote.volume_up() 
remote.volume_up() 
remote.channel_up() 
remote.mute() 
remote.toggle_power() 
print("\n" + "-" * 50 + "\n") 
tv2 = SamsungTV() 
print() 
adv_remote = AdvancedRemote(tv2) 
adv_remote.toggle_power() 
adv_remote.set_channel(42) 
adv_remote.volume_up() 
adv_remote.channel_down() 
adv_remote.toggle_power() 
if __name__ == "__main__": 
main() 
