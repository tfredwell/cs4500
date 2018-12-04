from asyncio import sleep

import cozmo

from cozmo_taste_game.robot import EvtWrongFood, EvtCorrectFood, EvtUnknownTag, EvtNewGameStarted


class RealTasterBot:
    def __init__(self):
        self.cozmo = None
        self.world = None

    async def run(self, connection):
        try:
            self.cozmo = await connection.wait_for_robot()
            self.world = self.cozmo.world
            print('runnint')
            while True:
                await sleep(0.1)
        except KeyboardInterrupt:
            print("Exited.")

    async def __start_new_game(self, evt: EvtNewGameStarted, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        action = self.cozmo.say_text(f'I am hungry for some {evt.food_group.name}')
        await action.wait_for_completed()

    async def __unknown_tag(self, evt: EvtUnknownTag, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        action = self.cozmo.say_text('Hmm, I do not know what that is!')
        await action.wait_for_completed()
        self.ready = True

    async def __wrong_food(self, evt: EvtWrongFood, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        say = self.cozmo.say_text(f'A {evt.food_item.name} is not a {evt.expected_food_group.name}')
        await say.wait_for_completed()

    async def __correct_food(self, evt: EvtCorrectFood, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        msg = f'Yum! The {evt.food_item.food_group.name} {evt.food_item.name} is {evt.food_item.taste}'
        action = self.cozmo.say_text(msg, play_excited_animation=True)
        await action.wait_for_completed()

    def connect(self, engine):
        engine.add_event_hander(EvtNewGameStarted, self.__start_new_game)
        engine.add_event_hander(EvtUnknownTag, self.__unknown_tag)
        engine.add_event_hander(EvtWrongFood, self.__wrong_food)
        engine.add_event_hander(EvtCorrectFood, self.__correct_food)

