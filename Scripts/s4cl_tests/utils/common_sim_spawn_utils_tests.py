"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils


@CommonTestService.test_class(ModInfo.get_identity())
class _CommonSimSpawnUtilsTests:
    @staticmethod
    @CommonTestService.test()
    def _should_spawn_and_despawn_human_sim_properly() -> None:
        sim_info = CommonSimSpawnUtils.create_human_sim_info(first_name='Tester', last_name='McTest', source='testing')
        try:
            CommonAssertionUtils.is_true(sim_info is not None)
            CommonAssertionUtils.is_true(CommonSimSpawnUtils.despawn_sim(sim_info, cause='S4CL Testing Despawn.'))
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info, source='S4CL Test Clean Up')

    @staticmethod
    @CommonTestService.test()
    def _should_spawn_and_despawn_large_dog_sim_properly() -> None:
        sim_info = CommonSimSpawnUtils.create_large_dog_sim_info(first_name='Tester', last_name='McTest', source='testing')
        try:
            CommonAssertionUtils.is_true(sim_info is not None)
            CommonAssertionUtils.is_true(CommonSimSpawnUtils.despawn_sim(sim_info, cause='S4CL Testing Despawn.'))
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info, source='S4CL Test Clean Up')

    @staticmethod
    @CommonTestService.test()
    def _should_spawn_and_despawn_small_dog_sim_properly() -> None:
        sim_info = CommonSimSpawnUtils.create_small_dog_sim_info(first_name='Tester', last_name='McTest', source='testing')
        try:
            CommonAssertionUtils.is_true(sim_info is not None)
            CommonAssertionUtils.is_true(CommonSimSpawnUtils.despawn_sim(sim_info, cause='S4CL Testing Despawn.'))
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info, source='S4CL Test Clean Up')

    @staticmethod
    @CommonTestService.test()
    def _should_spawn_and_despawn_fox_sim_properly() -> None:
        sim_info = CommonSimSpawnUtils.create_fox_sim_info(first_name='Tester', last_name='McTest', source='testing')
        try:
            CommonAssertionUtils.is_true(sim_info is not None)
            CommonAssertionUtils.is_true(CommonSimSpawnUtils.despawn_sim(sim_info, cause='S4CL Testing Despawn.'))
        finally:
            CommonSimSpawnUtils.delete_sim(sim_info, source='S4CL Test Clean Up')

