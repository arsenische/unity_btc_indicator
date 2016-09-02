#! /usr/bin/env python
# This script adds bitcoin price indicator to the unity tray (and refreshes it every 10 seconds) thanks to:
#   https://bitcoinaverage.com
#   http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
#   https://jbernard.io/2010/04/16/periodic-timers-in-pygtk.html
# Todo: replace curl with some python-site 

APPINDICATOR_ID = 'BtcRate'

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GObject as gobject

class RateUpdater:
  def __init__(self, timeout):
    import os
    self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('btc.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    self.callback()
    gobject.timeout_add_seconds(timeout, self.callback)

  def callback(self):
    self.indicator.set_status(appindicator.IndicatorStatus.ATTENTION)
    self.indicator.set_label('$'+str(get_btc_rate()), 'hehe')
    self.indicator.set_menu(build_menu())
    return True

def main():
  rate_updater = RateUpdater(10)
  import signal
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  gtk.main()

def build_menu():
  menu = gtk.Menu()
  item_quit = gtk.MenuItem('Quit')
  item_quit.connect('activate', quit)
  menu.append(item_quit)
  menu.show_all()
  return menu

def get_btc_rate():
  import urllib
  url = "https://api.bitcoinaverage.com/ticker/global/USD/"
  response = urllib.urlopen(url)
  import json
  btc_rate = json.loads(response.read())['last']
  return btc_rate

def quit(source):
  gtk.main_quit()

if __name__ == "__main__":
  main()
