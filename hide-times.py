__addon_name__ = "Hide Button Times"
__version__ = "1.1"

from aqt import mw, dialogs
from aqt.utils import showInfo
from aqt.qt import *
from aqt import appVersion
from aqt.utils import showWarning

from anki.hooks import addHook
import aqt

ht_state_on = False
ht_menu = None
ht_profile_loaded = False

def shownButtonTime(self, i):
    if not self.mw.col.conf['estTimes']:
        return "<div class=spacer></div>"
    txt = self.mw.col.sched.nextIvlStr(self.card, i, True) or "&nbsp;"
    return '<span class=nobold>%s</span><br>' % txt

def hiddenButtonTime(self, i): 
    return "<span class=nobold>Press %d</span><br>" %i

def ht_on():
    if not ht_profile_loaded:
        showWarning(HT_ERROR_NO_PROFILE)
        return False
    try:
        global ht_state_on
        ht_state_on = True

        aqt.reviewer.Reviewer._buttonTime = hiddenButtonTime
        ht_menu.setChecked(True)
        return True
    except:
        showWarning(HT_ERROR_SWITCH)
        return False


def ht_off():
    if not ht_profile_loaded:
        showWarning(HT_ERROR_NO_PROFILE)
        return False
    try:
        global ht_state_on
        ht_state_on = False

        aqt.reviewer.Reviewer._buttonTime = shownButtonTime
        ht_menu.setChecked(False)
        return True
    except:
        showWarning(HT_ERROR_SWITCH)
        return False

HT_ERROR_SWITCH = """ Switching the times during review failed: This is a really
simple program, so it should be fixed by waiting a bit."""
HT_ERROR_NO_PROFILE = """ Switching the times during review failed: The profile
has not yet been loaded. It could be a bug in Anki or it might be fixed by
waiting a bit."""

def ht_switch():
    is_active_dialog = filter(bool, [x[1] for x in dialogs._dialogs.values()])

    if appVersion.startswith('2.0') and is_active_dialog:
        info = _("Send Help; Dialogs has too many bugs")
        showWarning(info)
        print(info)
    else:
        if ht_state_on:
            ht_off()
        else:
            ht_on()

def ht_save():
    mw.pm.profile['ht_state_on'] = ht_state_on

def ht_load():
    global ht_state_on, ht_profile_loaded

    try:
        ht_state_on = mw.pm.profile['ht_state_on']

    except KeyError: 
        ht_state_on = False

    ht_profile_loaded = True

    if ht_state_on:
        ht_on()

def ht_init():
    global ht_menu
    addHook("profileLoaded",ht_load)
    addHook("unloadProfile",ht_save)
    ht_menu = QAction("Hide Button Times", mw, checkable=True)
    ht_menu.triggered.connect(ht_switch)
    try:
        mw.addon_view_menu
    except AttributeError:
        mw.addon_view_menu = QMenu(_(u"&View"), mw)
        mw.form.menubar.insertMenu(mw.form.menuTools.menuAction(),
                                   mw.addon_view_menu)
        mw.addon_view_menu.addAction(ht_menu)

ht_init()
