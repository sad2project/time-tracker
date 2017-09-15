from configuration import Configuration


test_file_location = "C:\Users\Jake\Programming\Time Tracker\samplefiles\time_tracker.config"


def find_task_in_file(taskname):
    with open(test_file_location, 'r') as file:
        file.r


def test_add_task_to_config():
    config = Configuration(test_file_location)

    config.addTask('test', 0)

    #determine that the task is in the config