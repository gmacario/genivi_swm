# (c) 2015 - Jaguar Land Rover.
#
# Mozilla Public License 2.0
#
# Python-based package manager PoC



import gtk
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import sys
import time

#
# Package manager service
#
class PkgMgrService(dbus.service.Object):
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.slm_bus_name = dbus.service.BusName('org.genivi.package_manager', 
                                                 bus=self.bus)
        dbus.service.Object.__init__(self, 
                                     self.slm_bus_name, 
                                     '/org/genivi/package_manager')


    def send_operation_result(self, transaction_id, result_code, result_text):
        #
        # Retrieve software loading manager bus name, object, 
        # and installation report method
        #
        slm_bus_name = dbus.service.BusName('org.genivi.software_loading_manager', 
                                            bus=self.bus)
        slm_obj = self.bus.get_object(slm_bus_name.get_name(), 
                                      "/org/genivi/software_loading_manager")

        slm_operation_result = slm_obj.get_dbus_method("operation_result", 
                                                       "org.genivi.software_loading_manager")
        
        #
        # Send back operation result.
        # Software Loading Manager will distribute the report
        # to all interested parties.
        #
        print "Will send back {} {}/{}".format(transaction_id, result_code, result_text)
        slm_operation_result(transaction_id, result_code, result_text)
        print "Sent"
        return None

    @dbus.service.method('org.genivi.package_manager',
                         async_callbacks=('send_reply', 'send_error'))
    def install_package(self, 
                        transaction_id,
                        image_path,
                        blacklisted_packages,
                        send_reply, 
                        send_error): 

        print "Package Manager: Got install_package()"
        print "  Operation Transaction ID: {}".format(transaction_id)
        print "  Image Path:               {}".format(image_path)
        print "  Blacklisted packages:     {}".format(blacklisted_packages)
        print "---"

        #
        # Send back an immediate reply since DBUS
        # doesn't like python dbus-invoked methods to do 
        # their own calls (nested calls).
        #
        send_reply(True)

        # Simulate install
        print "Intalling package :"
        for i in xrange(1,10):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.2)
        print  
        print "Done"
        self.send_operation_result(transaction_id,
                                   0,
                                   "Installation successful")                                 

        return None

    @dbus.service.method('org.genivi.package_manager',
                         async_callbacks=('send_reply', 'send_error'))
    def upgrade_package(self, 
                        transaction_id,
                        image_path,
                        blacklisted_packages,
                        send_reply, 
                        send_error): 

        print "Package Manager: Got upgrade_package()"
        print "  Operation Transaction ID: {}".format(transaction_id)
        print "  Image Path:               {}".format(image_path)
        print "  Blacklisted packages:     {}".format(blacklisted_packages)
        print "---"

        #
        # Send back an immediate reply since DBUS
        # doesn't like python dbus-invoked methods to do 
        # their own calls (nested calls).
        #
        send_reply(True)

        # Simulate install
        print "Upgrading package :"
        for i in xrange(1,10):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.2)
        print  
        print "Done"
        self.send_operation_result(transaction_id,
                                   0,
                                   "Upgrade successful")

        return None

    @dbus.service.method('org.genivi.package_manager',
                         async_callbacks=('send_reply', 'send_error'))
    def remove_package(self, 
                       transaction_id,
                       package_id,
                       send_reply, 
                       send_error): 
        print "Package Manager: Remove package upgrade_package()"
        print "  Operation Transaction ID: {}".format(transaction_id)
        print "  Package ID:               {}".format(package_id)
        print "---"

        #
        # Send back an immediate reply since DBUS
        # doesn't like python dbus-invoked methods to do 
        # their own calls (nested calls).
        #
        send_reply(True)

        # Simulate install
        print "Removing package:"
        for i in xrange(1,10):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.2)
        print  
        print "Done"
        self.send_operation_result(transaction_id,
                                   0,
                                   "Removal successful")                                 

        return None

    @dbus.service.method('org.genivi.package_manager')
    def get_installed_packages(self): 
        print "Got get_installed_packages()"
        return [ 'bluez_driver_1.2.2', 'bluez_apps_2.4.4' ]
                 


print 
print "Package Manager."
print


DBusGMainLoop(set_as_default=True)
pkg_mgr = PkgMgrService()

while True:
    gtk.main_iteration()
