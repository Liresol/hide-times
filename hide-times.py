__addon_name__ = "Hide Button Times"
__version__ = "1.0"

from aqt import mw, dialogs
from aqt.utils import showInfo
from aqt.qt import *
from aqt import appVersion
from aqt.utils import showWarning
import aqt

ht_state_on = False
ht_menu = None

def shownButtonTime(self, i):
    if not self.mw.col.conf['estTimes']:
        return "<div class=spacer></div>"
    txt = self.mw.col.sched.nextIvlStr(self.card, i, True) or "&nbsp;"
    return '<span class=nobold>%s</span><br>' % txt

def hiddenButtonTime(self, i): 
    return "<span class=nobold>Press %d</span><br>" %i

def ht_on():
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
    try:
        global ht_state_on
        ht_state_on = False

        aqt.reviewer.Reviewer._buttonTime = shownButtonTime
        ht_menu.setChecked(False)
        return True
    except:
        showWarning(HT_ERROR_SWITCH)
        return False

HT_ERROR_SWITCH = """ Switching the times during review failed: This is a really simple program, so someone really skrewed up."""

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

def ht_init():
    global ht_menu
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
