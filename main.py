import pymem
import time
import keyboard

pm = pymem.Pymem("hdeep.exe")
client = pymem.process.module_from_name(pm.process_handle, 'hdeep.exe')

clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
clientBase = client.lpBaseOfDll
dwLocalPlayer = 0x3EB5D8
dwGameInfo = 0x3E8678
dwGameStats = 0x3EB740
dwTime = 0x3EB640
dwMurphy = 0x407FE0  # need to use same char length as "Murphy"[6]
dwPlayerType = 0x4100B0  # need to use same char length as "Scout"[5]
dwGameSettings = 0x44FAB0

m_iWeapon = 0x1F0  # int
m_iAmmo = 0x40  # int # needs the m_iWeapon offset first

m_iDeaths = 0xA0  # int

m_iHealth = 0x1B0  # float

m_iStatsPlayer = 0x38
m_iHealthLost = 0x20

m_iStatsWorld = 0x2C
m_iShotsFired = 0x22

m_iInventory = 0x1A0
m_iItem = 0x0C  # is used by inventory and iStats

m_iScanBalls = 0x28
m_iItemsLeft = 0x14
m_iIsRunning = 0x18  # uses dwGameSettings


def main():
    print("Started main cheat")
    setMurphy("CHEATS")
    setPlayerType("1337x")
    while True:
        setHealth(999.0)
        setAmmo(999)
        setScanBalls(999)
        time.sleep(5)


def setHealth(value: float):
    localPlayer = pm.read_int(clientBase + dwLocalPlayer)
    pm.write_float(localPlayer + m_iHealth, value)


def setAmmo(value: int):
    localPlayer = pm.read_int(clientBase + dwLocalPlayer)
    weapon = pm.read_int(localPlayer + m_iWeapon)
    pm.write_int(weapon + m_iAmmo, value)


def setScanBalls(value: int):
    localPlayer = pm.read_int(clientBase + dwLocalPlayer)
    inventory = pm.read_int(localPlayer + m_iInventory)
    item = pm.read_int(inventory + m_iItem)
    scanBallsInv = pm.read_int(item + m_iScanBalls)
    pm.write_int(scanBallsInv + m_iItemsLeft, value)


def setMurphy(value: str):
    pm.write_bytes(clientBase + dwMurphy, value.encode(encoding="UTF-16"),  len(value.encode(encoding="UTF-16")))


def setPlayerType(value: str):
    pm.write_bytes(clientBase + dwPlayerType, value.encode(encoding="UTF-16"),  len(value.encode(encoding="UTF-16")))


def setTime(value: int):
    pm.write_int(clientBase + dwTime, value)


def setDeaths(value: int):
    gameInfo = pm.read_int(clientBase + dwGameInfo)
    pm.write_int(gameInfo + m_iDeaths, value)


# def setShotsFired(value: int):
#     gameStats = pm.read_int(clientBase + dwGameStats)
#     stats = pm.read_int(gameStats + m_iStats)
#     pm.write_int(stats + m_iShotsFired, value)

def setHealthLoss(value: int):
    gameStats = pm.read_int(clientBase + dwGameStats)
    stats = pm.read_int(gameStats + m_iStatsPlayer)
    pm.write_int(stats + m_iHealthLost, value)


def resetStats(): # Setting time doesn't work
    setTime(5000)
    time.sleep(1)
    setDeaths(0)
    time.sleep(1)
    setHealthLoss(0)


while True:
    if keyboard.is_pressed("F1"):
        main()



    time.sleep(0.01)
