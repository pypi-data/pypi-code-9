"""
Created on Feb 11, 2015

@author: Jason Bowles
"""
from rawdata_emca.runner.config_entry import ConfigEntry
from ConfigParser import SafeConfigParser
from rawdata_emca.utilities import RawDataUtilities
from rawdata_emca.utilities.factory import create_entry
from rawdata_emca import Base_Type
import copy

class ConfigFileReader(Base_Type):
    """
    The config file reader reads in the config files found in the directories passed
    
    For each entry in a config file, it will create a ConfigEntry instance, which then can run the Processor or Connector
    and handle the output
    
    Here is the idea behind dependencies and successors
    If an entry has a dependency.. then if that dependency is also running as part of the schedule, the entry will run after that.. 
       if the dependency is not scheduled.. then the job will run as if it did not have any dependencies
       Successors are only used if you want to chain some entries together, if a config entry doesn't exist.. the 
         non-std options will be passed to that successor (in this case the successor name will need to be the src_implementation
         
        RIGHT NOW... SUCCESSORS have not been implemented yet.. may never be..
        
    THere can be more than one dependency and successor
    If you have a connector and a processor - you do not need dependencies (they are run separately by default)
       successors and dependencies only work within connectors and within processors
    """
    entries = {}
    
    source_files = {}
    entry_dict = {}
    run_date = RawDataUtilities.get_now()
    entry_types = {Base_Type.CONNECTOR:0,Base_Type.PROCESSOR:1}
    
    ##
    #  These options determine basic functionality
    # Changing behavior would requre the changing of how these options are used
    # standard options do not get passed down to the instantiation directly
    #   - but they are accessible through the entry.. which is accessible
    standard_options = ['description',
                        'connection_type',
                        'last_processed',
                        'num_run',
                        'out_filename',
                        'src_implementation',
                        'run_frequency',
                        'temp_results', 
                        'working_directory',
                        'dependencies',
                        'successors',
                        'file_write',
        #                'entry_type',
                        'last_run'] 
    
    # update the updates dictionary to be used
    USED = '$$$$$   USED   $$$$$'

    def __init__(self, params):
        """
        Constructor
        """
        Base_Type.__init__(self)
        if 'run_date' in params:
            self.run_date = RawDataUtilities.date_from_string(params['run_date'])
        
        self.entry_name = params.get('entry_name',None)
        self.total_time = 0.0
        
        self.entries[0] = []
        self.entries[1] = []
        
        #self.set_uuid(params.get('uuid','---none---'))
        self.log_message("Initialization Complete", log_type='main', status='running', step='load configs',name='config_file_reader',log_level=self.log_info())
    
    def execute_entries(self):
        """
        iterate through entries and run them
        """
        self.order_entries()
        self.ent_result = {}
        start_time = RawDataUtilities.get_now()
        self.log_message("Now preparing to run config entries",status='start',step='execute entries')
        for i in xrange(len(self.entries)):
            if len(self.entries[i]) > 0:
                self.log_message('processing all configs of type: '+str(self.entries[i][0].get_entry_type())+", now..",status='running',name='congig_file_reader')
            for ent in self.entries[i]:
                if self.do_run(ent):
                    self.log_message(' About to run: '+ent.name, name=ent.name)
                    print "... running... "+ent.name
                    ent.execute_entry()
                    self.total_time = RawDataUtilities.get_diff(start_time,seconds=True)
                    self.ent_result[ent.name] = ent.return_val
                    ent.updates['last_processed'] = RawDataUtilities.string_from_date(RawDataUtilities.add_seconds_to_date(self.run_date, self.total_time))
                    
        
        self.log_message("All entries have run",status='complete')
        total_ret = self.log_summary(self.update_all_configs())
        return total_ret
    
    def do_run(self, _entry):
        """
        supports the regular framework run and a single entry run from the command line
        """
        if self.entry_name:
            return _entry.name == self.entry_name
        if _entry.run_now(self.run_date):
            for dep in _entry.dependencies:
                ## check if a prior run failed or didn't run because of a previous failure
                if self.dep_error(_entry, dep, self.entries[self.entry_types[Base_Type.CONNECTOR]]) or \
                   self.dep_error(_entry, dep, self.entries[self.entry_types[Base_Type.PROCESSOR]]):      
                    return False
            return True
                             
        #return _entry.run_now(self.run_date)
        return False
    
    def dep_error(self, _entry, _dep, _entries):
        """
        This section of code is designed to determine if the entry should not run based on the results of a dependency
        As of 4/7/2015 there are 3 reasons why an entry can not run because of a dependency problem
        1) The last run of a dependency ended in "failure"
        2) The current run of the dependency failed
        3) The dependency has not ran since the last run of the entry (ensures not re-running a duplicate through)
         --- this is not a concern if everything is set to "New" in your chain
        """
        for ent in _entries: # processors
            if _dep == ent.name:
                if ent.return_val == None:
                    if ent.last_run == 'failure':
                        self.log_message("Not running entry ("+_entry.name+"): because of a prior failure of dependency: "+_dep)
                        _entry.no_run_reason = "A Dependency is still in a failed status"
                        return True
                    elif not _entry.first_run and _entry.last_processed >= ent.last_processed:
                        self.log_message("No running entry ("+_entry.name+"): because dependency has not run since last run: "+_dep)
                        _entry.no_run_reason = "A dependency last run is still before this instance's last run"
                        return True
                if ent.return_val > 0:
                    self.log_message("Not running entry ("+_entry.name+"): because of a dependency failed: "+_dep)
                    _entry.no_run_reason = "A Dependency failed"
                    return True
        return False
    
    def log_summary(self, no_run_list):
        """
        Wrap up the log entry and summarize why entries did not run if they were found
        """
        self.log_message('Entries not run' ,step='summary',status='start',name='config_file_reader')
        for name in no_run_list.keys():
            self.log_message('Did not run: '+name+', '+no_run_list[name],status='running')
        
        ret_total = 0
        for x in xrange(2):
            for ent in self.entries[x]:
                ret_total = ret_total + 0 if ent.return_val == None else ent.return_val
        self.log_message('Summary Complete, Run Time = ('+str(self.total_time)+')',status='complete')
        return ret_total
    
    def order_entries(self):
        """
        Go through the connectors and processors and if there is more than 1.. we'll create a kicker to start off that 
          group of entries and then order the rest
        """
        for key in self.entries.keys():
            entry_set = self.entries[key]
            if len(entry_set) > 0:
                sorted_set = self.order_entry_set(entry_set)
                self.entries[key] = sorted_set
        
    def order_entry_set(self, entry_set):
        """
        Create the kicker which will start all of the execution
        
        Then look for entries that have more than 1 dependency (all will have kicker as dependency.. except well .. kicker
        If they don't have more than 1, put that in the no_dep dictionary with their order number (should be 1) .. kicker will be 0
        
        Now loop through the dependency list removing each until the all dependencies have been identified and placed in the schedule
        then adding to the dependency dictionary..  this will go into a loop if 2 entries depend on each other.. If you do this.. you are a doofus!
        """
        kicker = self.clone_entry(entry_set[0])
        ret_set = []
        ret_set.append(kicker)
        no_dep = {}
        no_dep[kicker.name] = kicker.order
        
        dep = []
        _all = []
        for c_entry in entry_set:
            c_entry.order = 1
            _all.append(c_entry.name)
            if len(c_entry.dependencies) > 1:
                dep.append(c_entry)
            else:
                no_dep[c_entry.name] = c_entry.order
                ret_set.append(c_entry)
        
        while len(dep) > 0:
            for c_entry in dep:
                dl = copy.copy(c_entry.dependencies)
                for d in c_entry.dependencies:
                    if d == 'kicker':
                        """ the kicker of everything """
                        dl.remove(d)
                    elif not d in _all:
                        """ not scheduled today """
                        dl.remove(d)
                    elif d in no_dep:
                        """ found the dependency in the schedule.. make sure the order is at least 1 more than that """
                        dl.remove(d)
                        if not c_entry.order > no_dep[d]:
                            c_entry.order = no_dep[d] + 1

                if len(dl) == 0:
                    no_dep[c_entry.name] = c_entry.order
                    ret_set.append(c_entry)
                    dep.remove(c_entry)
                    
                    
        return sorted(ret_set, key=lambda c_entry: c_entry.order)
                
    def clone_entry(self, c_entry):
        kicker = copy.copy(c_entry)
        kicker.name = 'kicker'
        kicker.out_filename = 'kicker.csv'
        kicker.file_write = "Append"
        kicker.description = 'An entry designed to just start the process'
        instance = create_entry('kicker',c_entry.get_entry_type())
        instance.entry = kicker
        kicker.instance = instance
        kicker.dependencies = []
        kicker.run_frequency = 'Every'
        kicker.last_run = 'success'
        kicker.source_file = None
        kicker.temp_results = 'None'
        kicker.return_val = 0
        kicker.last_processed = RawDataUtilities.get_now()
        kicker.order = 0
        return kicker
         
    def process_config(self, filename):
        """
        the config file reader can process multiple config files
        """
        
        self.log_message("processing config file: "+filename)
        parser = SafeConfigParser()
        parser.read(filename)
        self.source_files[filename] = parser
        
        sections = parser.sections()
        for section in sections:
            
            options = parser.options(section)
            params = {}
            non_std = {}
            for option in options:
                ## any option that ends with the word "password" will be encrypted and will automatically be decrypted upon
                ## processing        
                if option in self.standard_options:
                    params[option] = self.get_value(option, parser.get(section, option))
                else:
                    non_std[option] =  self.get_value(option, parser.get(section, option))

            params['non_std'] = non_std
            params['source_file'] = filename
            params['name']=section
            params['run_date']=self.run_date
            c_entry = ConfigEntry(params)
            if c_entry.ready: 
                entry_num = c_entry.get_entry_type()
                self.entries[self.entry_types[entry_num]].append(c_entry)
                self.entry_dict[section] = filename
                self.log_message("Loaded Config Entry: "+section)
            else:
                self.log_message("Failed to load config entry: "+section)

        return self.entries
    
    def get_value(self, option, option_val):
        """
        If this is a password entry it must end with "password", then the framework will decrypt it
        otherwise it assumes there was no decryption needed
        """
        if option.endswith('password'):
            return RawDataUtilities.decrypt_password(option_val)
        return option_val
    
    def update_all_configs(self):
        self.log_message("Update Entries",status='start',step='update configs')
        all_updates = {}
        no_run = {}
        for key in self.entries.keys():
            entry_list = self.entries[key]
            for c_entry in entry_list:
                if c_entry.name in self.ent_result and not c_entry.name == 'kicker':
                    if self.ent_result[c_entry.name] == 0:
                        all_updates[c_entry.name] = c_entry.updates
                        all_updates[c_entry.name]['last_run'] = 'success'
                    else:
                        msg = ' (Failure) Not updating: '+c_entry.name
                        if c_entry.instance.message:
                            msg = msg + ", Message: ("+c_entry.instance.message+")"
                        self.log_message(msg,name=c_entry.name,status='error',log_level=self.log_error())
                        all_updates[c_entry.name] = {'last_run':'failure'}
                else:
                    if not c_entry.name == 'kicker':
                        no_run[c_entry.name] = c_entry.no_run_reason
        
        for name in all_updates.keys():
            self.log_message('Updating config file for: '+name,name=name, status='running')
            self.update_config(name, all_updates[name], self.source_files[self.entry_dict[name]])
            
        ## write out updates for each config file
        for sf in self.source_files:
            parser = self.source_files[sf]
            with open(sf, 'w') as configfile:
                parser.write(configfile)
        
        self.log_message('All config files updated',status='complete')
        return no_run
            
    
    def update_config(self, entry_name, entry_updates, parser): 

        for key in entry_updates.keys():
            parser.set(entry_name, key, entry_updates[key])
            
        