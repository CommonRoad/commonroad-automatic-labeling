from abc import abstractmethod

from commonroad.scenario.scenario import Scenario

from commonroad_labeling.common.tag import Tag, TagGroup


class AutoLabelingBase:
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self.tag_group = None

    def get_tags_contained_in_scenario(self) -> set[Tag]:
        scenario_tags = set()
        for tag in Tag:
            if Tag(tag).value.startswith(self.tag_group):
                if self.scenario_contains_tag(Tag(tag)):
                    scenario_tags.add(Tag(tag))

        return scenario_tags

    @abstractmethod
    def scenario_contains_tag(self, tag: Tag) -> bool:
        pass

    def assign_tag_to_scenario(self, tag: Tag):
        self.scenario.tags.add(tag)
