import obspython as obs
import os
import codecs
import patreon

file_path = ""
creator_id = ""
file_check_delay = 0
previous_missing_file = ""
previous_mtime = None
update_when_changed = False
loaded = False

def script_load(settings):
    global loaded
    scene = obs.obs_frontend_get_current_preview_scene() or obs.obs_frontend_get_current_scene()
    if scene:
        loaded = True
        obs.obs_source_release(scene)
    else:
        obs.obs_frontend_add_event_callback(frontend_event_cb)
        loaded = False

def frontend_event_cb(event):
    global loaded

    if event == obs.OBS_FRONTEND_EVENT_FINISHED_LOADING or event == obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGED:
        loaded = True
        read_file()
        obs.timer_add(read_file, file_check_delay)
        obs.remove_current_callback()

# SCRIPT PROPERTIES
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "creator_id", "Creator ID: ", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_path(props, "file_path", "File Path: ", obs.OBS_PATH_FILE, "*.txt", "")
    obs.obs_properties_add_int(props, "file_check_delay", "Check delay (ms):", 50, 2**31-1, 100)
    obs.obs_properties_add_bool(props, "update_when_changed", "Only update sources when file is modified")

    return props

# SCRIPT PROPERTIES DEFAULT VALUES
def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "file_check_delay", 1000)
    obs.obs_data_set_default_bool(settings, "update_when_changed", True)

def script_update(settings):
    global file_path
    global creator_id
    global file_check_delay
    global update_when_changed
    global previous_mtime

    new_file_path = obs.obs_data_get_string(settings, "file_path")
    new_creator_id = obs.obs_data_get_string(settings, "creator_id")
    new_file_check_delay = obs.obs_data_get_int(settings, "file_check_delay")
    update_when_changed = obs.obs_data_get_bool(settings, "update_when_changed")

    if not update_when_changed:
        previous_mtime = None

    if file_path != new_file_path:
        file_path = new_file_path
        creator_id = new_creator_id
        if loaded:
            read_file()
    if file_check_delay != new_file_check_delay and new_file_check_delay > 0:
        file_check_delay = new_file_check_delay
        if loaded:
            obs.timer_remove(read_file)
            obs.timer_add(read_file, file_check_delay)

# GET PATREON & WRITE IN FILE
def read_file():
    _read_file(file_path, creator_id)

def _read_file(file_path: str, creator_id: str):
    global previous_missing_file
    global previous_mtime

    if not file_path:
        print("returned file_path")
        return
    if not creator_id:
        print("returned creator_id")
        return
    try:
        if update_when_changed:
            mtime = os.stat(file_path).st_mtime
            if mtime == previous_mtime:
                return
            previous_mtime = mtime

            api_client = patreon.API(creator_id)
            campaign_id = api_client.fetch_campaign().data()[0].id()
            pledges_response = api_client.fetch_page_of_pledges(campaign_id,25,)

            names = []
            all_pledges = pledges_response.data()
            for pledge in all_pledges:
                patron_id = pledge.relationship('patron').id()
                patron = api_client.fetch_campaign_and_patrons().find_resource_by_type_and_id('user',patron_id)
                names.append(patron.attribute('full_name'))
            print(names)

            f = codecs.open(file_path, "w", "utf-8")
            for name in names:
                f.write(name + '\n')
            f.close()

    except FileNotFoundError as e:
        if previous_missing_file != file_path:
            print(e)
            previous_missing_file = file_path
            previous_mtime = None