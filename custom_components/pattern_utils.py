import re
from typing import Dict, List, Text, Union

import rasa.utils.io as io_utils
from rasa.nlu.training_data import TrainingData

def _convert_lookup_tables_to_regex(
    training_data: TrainingData, use_only_entities: bool = False
) -> List[Dict[Text, Text]]:
    """Convert the lookup tables from the training data to regex patterns.
    Args:
        training_data: The training data.
        use_only_entities: If True only regex features with a name equal to a entity
          are considered.

    Returns:
        A list of regex patterns.
    """
    patterns = []
    for table in training_data.lookup_tables:
        if use_only_entities and table["name"] not in training_data.entities:
            continue
        regex_pattern = _generate_lookup_regex(table)
        lookup_regex = {"name": table["name"], "pattern": regex_pattern}
        patterns.append(lookup_regex)
    return patterns


def _generate_lookup_regex(lookup_table: Dict[Text, Union[Text, List[Text]]]) -> Text:
    """Creates a regex pattern from the given lookup table.

    The lookup table is either a file or a list of entries.

    Args:
        lookup_table: The lookup table.

    Returns:
        The regex pattern.
    """
    lookup_elements = lookup_table["elements"]

    # if it's a list, it should be the elements directly
    if isinstance(lookup_elements, list):
        elements_to_regex = lookup_elements
    # otherwise it's a file path.
    else:
        elements_to_regex = _read_lookup_table_file(lookup_elements)

    # sanitize the regex, escape special characters
    elements_sanitized = [re.escape(e) for e in elements_to_regex]

    # regex matching elements with word boundaries on either side
    return "(\\b" + "\\b|\\b".join(elements_sanitized) + "\\b)"


def _read_lookup_table_file(lookup_table_file: Text) -> List[Text]:
    """Read the lookup table file.

    Args:
        lookup_table_file: the file path to the lookup table

    Returns:
        Elements listed in the lookup table file.
    """
    try:
        f = open(lookup_table_file, "r", encoding=io_utils.DEFAULT_ENCODING)
    except OSError:
        raise ValueError(
            f"Could not load lookup table {lookup_table_file}. "
            f"Please make sure you've provided the correct path."
        )

    elements_to_regex = []
    with f:
        for line in f:
            new_element = line.strip()
            if new_element:
                elements_to_regex.append(new_element)
    return elements_to_regex


def _collect_regex_features(
    training_data: TrainingData, use_only_entities: bool = False
) -> List[Dict[Text, Text]]:
    """Get regex features from training data.

    Args:
        training_data: The training data
        use_only_entities: If True only regex features with a name equal to a entity
          are considered.

    Returns:
        Regex features.
    """
    if not use_only_entities:
        return training_data.regex_features

    return [
        regex
        for regex in training_data.regex_features
        if regex["name"] in training_data.entities
    ]


def extract_patterns(
    training_data: TrainingData,
    use_lookup_tables: bool = True,
    use_regexes: bool = True,
    use_only_entities: bool = False,
) -> List[Dict[Text, Text]]:
    """Extract a list of patterns from the training data.

    The patterns are constructed using the regex features and lookup tables defined
    in the training data.

    Args:
        training_data: The training data.
        use_only_entities: If True only lookup tables and regex features with a name
          equal to a entity are considered.
        use_regexes: Boolean indicating whether to use regex features or not.
        use_lookup_tables: Boolean indicating whether to use lookup tables or not.

    Returns:
        The list of regex patterns.
    """

    #Adding names of entities which have a defined regex but 0 examples in trining data.    
    for regex in training_data.regex_features:
        training_data.entities.add(regex['name'])

    if not training_data.lookup_tables and not training_data.regex_features:
        return []

    patterns = []

    if use_regexes:
        patterns.extend(_collect_regex_features(training_data, use_only_entities))

    if use_lookup_tables:
        patterns.extend(
            _convert_lookup_tables_to_regex(training_data, use_only_entities)
        )

    return patterns