"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from typing import Union

from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_quaternion import CommonQuaternion
from sims4communitylib.classes.math.common_routing_location import CommonRoutingLocation
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_transform import CommonTransform
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
# ReadTheDocs
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if not ON_RTD:
    from autonomy.autonomy_component import AutonomyComponent
    from event_testing.results import EnqueueResult, TestResult
    import routing
    from routing import RoutingContext
    import objects.terrain
    from server.pick_info import PickType
    from placement import FGLSearchFlagsDefault, FGLSearchFlag
    from world.lot import Lot
    from sims.sim_info import SimInfo
else:
    # noinspection PyMissingOrEmptyDocstring
    class AutonomyComponent:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class EnqueueResult:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class TestResult:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class RoutingContext:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class PickType:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class FGLSearchFlagsDefault:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class FGLSearchFlag:
        STAY_IN_CURRENT_BLOCK = 0

    # noinspection PyMissingOrEmptyDocstring
    class Lot:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class SimInfo:
        pass


class CommonSimLocationUtils:
    """Utilities for manipulating the locations of Sims.

    """
    @staticmethod
    def get_position(sim_info: SimInfo) -> Union[CommonVector3, None]:
        """get_position(sim_info)

        Retrieve the current position of a Sim.

        :param sim_info: The Sim to get the position of.
        :type sim_info: SimInfo
        :return: The current position of the Sim or None if the Sim does not have a position.
        :rtype: Union[CommonVector3, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        # noinspection PyBroadException
        try:
            return CommonVector3.from_vector3(sim.position)
        except:
            return None

    @staticmethod
    def set_location(sim_info: SimInfo, location: CommonLocation) -> bool:
        """set_location(sim_info, location)

        Set the location of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param location: The location to put the Sim.
        :type location: CommonLocation
        :return: True, if the location of the Sim is successfully set. False, if not.
        :rtype: bool
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or location is None:
            return False
        # noinspection PyBroadException
        try:
            sim.location = location
        except:
            return False
        return True

    @staticmethod
    def get_location(sim_info: SimInfo) -> Union[CommonLocation, None]:
        """get_location(sim_info)

        Retrieve the current location of a Sim.

        :param sim_info: The Sim to get the location of.
        :type sim_info: SimInfo
        :return: The current location of the Sim or None if the Sim does not have a location.
        :rtype: Union[CommonLocation, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        # noinspection PyBroadException
        try:
            return CommonLocation.from_location(sim.location)
        except:
            return None

    @staticmethod
    def get_routing_location(sim_info: SimInfo) -> Union[CommonRoutingLocation, None]:
        """get_routing_location(sim_info)

        Retrieve a routing location for the current location of a Sim.

        :param sim_info: The Sim to get the location of.
        :type sim_info: SimInfo
        :return: The routing location for the current location of the Sim or None if the Sim does not have a location.
        :rtype: Union[CommonRoutingLocation, None]
        """
        sim_location = CommonSimLocationUtils.get_location(sim_info)
        if sim_location is None:
            return None
        return CommonRoutingLocation(sim_location.transform.translation, orientation=sim_location.transform.orientation, routing_surface=sim_location.routing_surface)

    @staticmethod
    def get_orientation(sim_info: SimInfo) -> CommonQuaternion:
        """get_orientation(sim_info)

        Retrieve the orientation of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The orientation of the Sim.
        :rtype: CommonQuaternion
        """
        if sim_info is None:
            return CommonQuaternion.empty()
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonQuaternion.empty()
        return CommonQuaternion.from_quaternion(sim.orientation)

    @staticmethod
    def get_orientation_degrees(sim_info: SimInfo) -> float:
        """get_orientation_degrees(sim_info)

        Retrieve the orientation of a Sim represented in degrees.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The orientation of the Sim represented in degrees.
        :rtype: float
        """
        return CommonQuaternion.to_degrees(CommonSimLocationUtils.get_orientation(sim_info))

    @staticmethod
    def get_routing_surface(sim_info: SimInfo) -> Union[CommonSurfaceIdentifier, None]:
        """get_routing_surface(sim_info)

        Retrieve the Routing Surface Identifier of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The Routing Surface Identifier of the specified Sim or None if a problem occurs.
        :rtype: Union[CommonSurfaceIdentifier, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None

        return CommonSurfaceIdentifier.from_surface_identifier(sim.routing_surface)

    @staticmethod
    def get_surface_level(sim_info: SimInfo) -> int:
        """get_surface_level(sim_info)

        Retrieve the Surface Level of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The Surface Level of the specified Sim or 0 if a problem occurs.
        :rtype: int
        """
        routing_surface = CommonSimLocationUtils.get_routing_surface(sim_info)
        if routing_surface is None:
            return 0
        return routing_surface.secondary_id

    @staticmethod
    def get_forward_vector(sim_info: SimInfo) -> CommonVector3:
        """get_forward_vector(sim_info)

        Retrieve the forward vector of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The forward vector of the Sim.
        :rtype: CommonVector3
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonVector3.empty()
        return CommonVector3.from_vector3(sim.forward)

    @staticmethod
    def get_routing_context(sim_info: SimInfo) -> Union[RoutingContext, None]:
        """get_routing_context(sim_info)

        Retrieve the routing context of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The routing context of the specified Sim or None if an error occurs.
        :rtype: Union[RoutingContext, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        return sim.routing_context

    @staticmethod
    def can_swim_at_location(sim_info: SimInfo, location: CommonLocation) -> bool:
        """can_swim_at_location(sim_info, location)

        Determine if a Sim can swim at the specified location.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param location: The Location to check.
        :type location: CommonLocation
        :return: True, if the Sim can swim at the specified location. False, if not.
        :rtype: bool
        """
        if location is None:
            return False
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        return sim.should_be_swimming_at_position(location.transform.translation, location.routing_surface.secondary_id)

    @staticmethod
    def can_swim_at_current_location(sim_info: SimInfo) -> bool:
        """can_swim_at_current_location(sim_info)

        Determine if a Sim can swim at their current location.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can swim at their current location. False, if not.
        :rtype: bool
        """
        location = CommonSimLocationUtils.get_location(sim_info)
        return CommonSimLocationUtils.can_swim_at_location(sim_info, location)

    @staticmethod
    def can_route_to_location(sim_info: SimInfo, location: CommonLocation) -> bool:
        """can_route_to_location(sim_info, location)

        Determine if a Sim can route to a Location.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param location: The location to route to.
        :type location: CommonLocation
        :return: True, if the Sim can route to the specified Location. False, if not.
        :rtype: bool
        """
        sim_routing_location = CommonSimLocationUtils.get_routing_location(sim_info)
        if sim_routing_location is None:
            return False
        sim_routing_context = CommonSimLocationUtils.get_routing_context(sim_info)
        if sim_routing_context is None:
            return False
        return routing.test_connectivity_pt_pt(sim_routing_location, CommonRoutingLocation.from_location(location), sim_routing_context)

    @staticmethod
    def can_route_to_position(sim_info: SimInfo, position: CommonVector3, routing_surface: CommonSurfaceIdentifier, orientation: CommonQuaternion=CommonQuaternion.empty()) -> bool:
        """can_route_to_position(sim_info, position, routing_surface)

        Determine if a Sim can route to a Location.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param position: The position to route to.
        :type position: CommonVector3
        :param routing_surface: The routing surface of the target.
        :type routing_surface: CommonSurfaceIdentifier
        :param orientation: The orientation of the position. Default is CommonQuaternion.empty().
        :type orientation: CommonQuaternion, optional
        :return: True, if the Sim can route to the specified Position. False, if not.
        :rtype: bool
        """
        location = CommonLocation(
            CommonTransform(
                position,
                orientation or CommonQuaternion.empty()
            ),
            routing_surface
        )
        return CommonSimLocationUtils.can_route_to_location(sim_info, location)

    @staticmethod
    def is_within_range_of_position(sim_info: SimInfo, position: CommonVector3, distance_in_squares: float) -> bool:
        """is_within_range_of_position(sim_info, position, distance_in_squares)

        Determine if a Sim is within a certain distance of a Position.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param position: A position.
        :type position: CommonVector3
        :param distance_in_squares: A unit measured in squares. 1 square is the size of 1 square in the Build/Buy mode visual grid. For comparison, a dining chair would be 1 square by 1 square. 0.5 would be half a square, or half a dining chair.
        :type distance_in_squares: float
        :return: True, if the distance between the Sim and the Position is less than or equal to the specified distance in squares. False, if not.
        :return: bool
        """
        sim_position = CommonSimLocationUtils.get_position(sim_info)
        if sim_position is None:
            return False
        return CommonLocationUtils.is_position_within_range_of_position(sim_position, position, distance_in_squares)

    @staticmethod
    def is_within_range_of_location(sim_info: SimInfo, location: CommonLocation, distance_in_squares: float) -> bool:
        """is_within_range_of_location(sim_info, location, distance_in_squares)

        Determine if a Sim is within a certain distance of a Location.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param location: A location.
        :type location: CommonLocation
        :param distance_in_squares: A unit measured in squares. 1 square is the size of 1 square in the Build/Buy mode visual grid. For comparison, a dining chair would be 1 square by 1 square. 0.5 would be half a square, or half a dining chair.
        :type distance_in_squares: float
        :return: True, if the distance between the Sim and the Location is less than or equal to the specified distance in squares. False, if not.
        :return: bool
        """
        sim_location = CommonSimLocationUtils.get_location(sim_info)
        if sim_location is None:
            return False
        return CommonLocationUtils.is_location_within_range_of_location(sim_location, location, distance_in_squares)

    @staticmethod
    def is_on_current_lot(sim_info: SimInfo) -> bool:
        """is_on_current_lot(sim_info)

        Determine if a Sim is on the active Lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is on the active Lot. False, if not.
        :rtype: bool
        """
        active_lot = CommonLocationUtils.get_current_lot()
        return CommonSimLocationUtils.is_on_lot(sim_info, active_lot)

    @staticmethod
    def is_on_lot(sim_info: SimInfo, lot: Lot) -> bool:
        """is_on_lot(sim_info, lot)

        Determine if a Sim is on a Lot.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param lot: An instance of a Lot.
        :type lot: Lot
        :return: True, if the Sim is on the specified Lot. False, if not.
        :rtype: bool
        """
        sim_position = CommonSimLocationUtils.get_position(sim_info)
        if sim_position is None:
            return False
        return CommonLocationUtils.is_position_on_lot(sim_position, lot)

    @staticmethod
    def is_renting_current_lot(sim_info: SimInfo) -> bool:
        """is_renting_current_lot(sim_info)

        Determine if a Sim is renting the current lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is renting the active lot. False, if not.
        :rtype: bool
        """
        return sim_info.is_renting_zone(CommonLocationUtils.get_current_zone_id())

    @staticmethod
    def is_at_home(sim_info: SimInfo) -> bool:
        """is_at_home(sim_info)

        Determine if a Sim is on their home Lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is on their home Lot. False, if not.
        :rtype: bool
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or not CommonHouseholdUtils.has_household(sim_info):
            return False
        return sim.on_home_lot or (CommonLocationUtils.get_current_zone_id() == CommonHouseholdUtils.get_household_zone_id(sim_info) and CommonSimLocationUtils.is_on_current_lot(sim_info))

    @staticmethod
    def send_to_position(sim_info: SimInfo, position: CommonVector3, level: int, go_here_interaction_id: int=None) -> EnqueueResult:
        """send_to_position(sim_info, position, level, go_here_interaction_id=None)

        Send a Sim to the specified position.

        :param sim_info: The Sim to send.
        :type sim_info: SimInfo
        :param position: The position to send the sim to.
        :type position: CommonVector3
        :param level: The level at which the position is located.
        :type level: int
        :param go_here_interaction_id: If supplied, this interaction will be used instead of the vanilla Go Here interaction. Default is None.
        :type go_here_interaction_id: int, optional
        :return: The result of sending the Sim to the specified position.
        :rtype: EnqueueResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return EnqueueResult(TestResult(False, 'No Sim was specified to be sent.'), None)
        from server_commands.sim_commands import _build_terrain_interaction_target_and_context, CommandTuning
        if position is None:
            return EnqueueResult(TestResult(False, 'No Position specified to send the Sim to!'), None)
        routing_surface = CommonSurfaceIdentifier.empty(secondary_id=level)
        (target, context) = _build_terrain_interaction_target_and_context(sim, position, routing_surface, PickType.PICK_TERRAIN, objects.terrain.TerrainPoint)
        if go_here_interaction_id is not None:
            return CommonSimInteractionUtils.queue_interaction(sim_info, go_here_interaction_id, target=target, interaction_context=context)
        return sim.push_super_affordance(CommandTuning.TERRAIN_GOHERE_AFFORDANCE, target, context)

    @staticmethod
    def send_near_position(sim_info: SimInfo, position: CommonVector3, level: int, go_here_interaction_id: int=None, position_search_flags: FGLSearchFlag=FGLSearchFlag.STAY_IN_CURRENT_BLOCK) -> EnqueueResult:
        """send_near_position(sim_info, position, level, go_here_interaction_id=None, position_search_flags=FGLSearchFlag.STAY_IN_CURRENT_BLOCK)

        Send a Sim near the specified position.

        :param sim_info: The Sim to send.
        :type sim_info: SimInfo
        :param position: The position to send the sim to.
        :type position: CommonVector3
        :param level: The level at which the position is located.
        :type level: int
        :param go_here_interaction_id: If supplied, this interaction will be used instead of the vanilla Go Here interaction. Default is None.
        :type go_here_interaction_id: int, optional
        :param position_search_flags: Flags used when locating a nearby position. Default is FGLSearchFlag.STAY_IN_CURRENT_BLOCK, which will limit the search to the current Room.
        :type position_search_flags: FGLSearchFlag, optional
        :return: The result of sending the Sim near the specified position.
        :rtype: EnqueueResult
        """
        if position is None:
            return EnqueueResult(TestResult(False, 'No Position specified to send the Sim to!'), None)

        transform = CommonTransform(position, CommonQuaternion.empty())
        location = CommonLocation(transform, CommonSurfaceIdentifier.empty(secondary_id=level))
        return CommonSimLocationUtils.send_near_location(sim_info, location, go_here_interaction_id=go_here_interaction_id, location_search_flags=position_search_flags)

    @staticmethod
    def send_to_location(sim_info: SimInfo, location: CommonLocation, go_here_interaction_id: int=None) -> EnqueueResult:
        """send_to_location(sim_info, location, go_here_interaction_id=None)

        Send a Sim to the specified location.

        :param sim_info: The Sim to send.
        :type sim_info: SimInfo
        :param location: The location to send the sim near to.
        :type location: CommonLocation
        :param go_here_interaction_id: If supplied, this interaction will be used instead of the vanilla Go Here interaction. Default is None.
        :type go_here_interaction_id: int, optional
        :return: The result of sending the Sim to the specified location.
        :rtype: EnqueueResult
        """
        if location is None:
            return EnqueueResult(TestResult(False, 'No Location specified to send the Sim to!'), None)

        position = location.transform.translation
        level = location.routing_surface.secondary_id
        return CommonSimLocationUtils.send_to_position(sim_info, position, level, go_here_interaction_id=go_here_interaction_id)

    @staticmethod
    def send_near_location(sim_info: SimInfo, location: CommonLocation, go_here_interaction_id: int=None, location_search_flags: FGLSearchFlag=FGLSearchFlag.STAY_IN_CURRENT_BLOCK) -> EnqueueResult:
        """send_near_location(sim_info, location, go_here_interaction_id=None, location_search_flags=FGLSearchFlag.STAY_IN_CURRENT_BLOCK)

        Send a Sim near the specified location.

        :param sim_info: The Sim to send.
        :type sim_info: SimInfo
        :param location: The location to send the sim near to.
        :type location: CommonLocation
        :param go_here_interaction_id: If supplied, this interaction will be used instead of the vanilla Go Here interaction. Default is None.
        :type go_here_interaction_id: int, optional
        :param location_search_flags: Flags used when locating a nearby location. Default is FGLSearchFlag.STAY_IN_CURRENT_BLOCK, which will limit the search to the current Room.
        :type location_search_flags: FGLSearchFlag, optional
        :return: The result of sending the Sim near the specified location.
        :rtype: EnqueueResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return EnqueueResult(TestResult(False, 'No Sim was specified to be sent.'), None)
        if location is None:
            return EnqueueResult(TestResult(False, 'No Location specified to send the Sim to!'), None)
        from placement import find_good_location, create_starting_location, create_fgl_context_for_sim
        routing_surface = location.routing_surface
        starting_location = create_starting_location(transform=location.transform, routing_surface=routing_surface)
        fgl_context = create_fgl_context_for_sim(starting_location, sim, search_flags=(FGLSearchFlagsDefault | location_search_flags) if location_search_flags is not None and location_search_flags != FGLSearchFlag.NONE else FGLSearchFlagsDefault)
        (position, orientation) = find_good_location(fgl_context)
        if position is None or orientation is None:
            fgl_context = create_fgl_context_for_sim(starting_location, sim)
            (position, orientation) = find_good_location(fgl_context)
        if position is not None and orientation is not None:
            transform = CommonTransform(position, orientation)
            location = CommonLocation(transform, starting_location.routing_surface)

        position = location.transform.translation
        level = location.routing_surface.secondary_id
        return CommonSimLocationUtils.send_to_position(sim_info, position, level, go_here_interaction_id=go_here_interaction_id)

    @staticmethod
    def is_allowed_on_current_lot(sim_info: SimInfo) -> bool:
        """is_allowed_on_current_lot(sim_info)

        Determine if a Sim is allowed on the current lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is allowed on the current lot. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.common_component_utils import CommonComponentUtils
        from sims4communitylib.enums.types.component_types import CommonComponentType
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        if CommonSimLocationUtils.is_at_home(sim_info):
            return True
        if CommonSimLocationUtils.is_renting_current_lot(sim_info):
            return True
        if CommonSimTypeUtils.is_player_sim(sim_info) and (CommonLocationUtils.current_venue_allows_role_state_routing() or not CommonLocationUtils.current_venue_requires_player_greeting()):
            return True
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        autonomy_component: AutonomyComponent = CommonComponentUtils.get_component(sim, CommonComponentType.AUTONOMY)
        if autonomy_component is None or not hasattr(autonomy_component, 'active_roles'):
            return False
        for role_state_instance in autonomy_component.active_roles():
            if CommonSimTypeUtils.is_non_player_sim(sim_info):
                if role_state_instance._portal_disallowance_tags or not role_state_instance._allow_npc_routing_on_active_lot:
                    return False
            elif role_state_instance._portal_disallowance_tags:
                return False
        return True
