#########################################################################
#class VService(object):
    #""""""

    ##----------------------------------------------------------------------
    #def __init__(self, module_name, control_host, control_port, bind_port, bind_if='',
                 #config=None, cryptor=None, result_query_interval=4):
        #"""Constructor"""
        ##
        ## identify
        ##
        #self._module_name = module_name
        #self._id = uuid.uuid1().hex
        
        ##
        ## platform ip/port
        ##
        #self._control_host = control_host
        #self._control_port = control_port
        
        ##
        ## local bind port
        ##
        #self._interface = bind_if
        #self._bind_port = bind_port
        
        ##
        ## cryptor
        ##
        #self._cryptor = cryptor
        
        ##
        ## config
        ##
        #self._config = VServiceConfig() if config == None else config
        #assert isinstance(self._config, VServiceConfig)
        
        ##
        ## add python env path
        ##
        #for _path in self._config.default_mod_paths:
            #sys.path.append(_path)
    
        #self._set_mod(self._module_name)
        
        ##
        ## connection/task/waiting ack pool
        ##
        #self._conn_pool = SDict(value={})
        #self._task_map = SDict(value={})
        
        ##
        ## result
        ##
        #self._result_buffer = SDict(value={}, new_kv_callback=self._notify_client)
        #self._update_result_loopingcall = LoopingCall(self._update_result)
        #self._update_result_loopingcall.start(result_query_interval)
    
    
    ##----------------------------------------------------------------------
    #def _set_mod(self, module_name):
        #""""""
        #if module_name:
            ##
            ## module_name not null
            ##
            #self._module_obj = __import__(self._module_name)
            #assert isinstance(self._module_name, types.ModuleType)
        
            ##
            ## build mod factory
            ##
            #_ = {}
            #for i in mod._MOD_ATTRS:
                #_[i] = getattr(self._config, i)
                
            #self._factory = mod.ModFactory(**_)
            
            #self._mod = self._factory.build_standard_mod_from_module(self._module_obj)
            #assert isinstance(self._mod, mod.ModStandard)
        #else:
            ##
            ## empty
            ##
            
            #_ = {}
            #for i in mod._MOD_ATTRS:
                #_[i] = getattr(self._config, i)
            
            #self._mod = mod.ModStandard(name=uuid.uuid1().hex, **_)
    
    ##----------------------------------------------------------------------
    #def load_from_module(self, module_name):
        #""""""
        #assert isinstance(self._mod, mod.ModStandard)
        #_module = __import__(module_name)
        #self._module_name = module_name
        #self._mod.from_module(_module)
        

    ##----------------------------------------------------------------------
    #def _notify_client(self, task_id, result):
        #""""""
        #_t = self._task_map.get(task_id)
        #if isinstance(_t, _TaskInServer):
            #_t.conn.send(actions.Result(task_id, result))
            
        #del self._result_buffer[task_id]
        #del self._task_map[task_id]

    ##----------------------------------------------------------------------
    #def _update_result(self):
        #""""""
        #_queue = self._mod.result_queue
        #while _queue.qsize() > 0:
            #try:
                #_r = _queue.get_nowait()
                #_ti = _r.get('task_id')
                #self._result_buffer[_ti] = _r
            #except queue.Empty:
                #break
        
    
    #@property
    #def mod(self):
        #""""""
        #return self._mod
    
    #@property
    #def factory(self):
        #""""""
        #return self._factory
    
    ##----------------------------------------------------------------------
    #def execute(self, params, task_id, cid):
        #""""""
        ##
        ## update task map
        ##
        #self._task_map[task_id] = _TaskInServer(task_id, cid, self.get_conn(
                                                                           #cid))
        
        ##
        ## execute
        ## 
        #self._mod.execute(params, task_id)
    
    ##----------------------------------------------------------------------
    #def serve(self):
        #""""""
        ##
        ## connect with platform
        ##
        #reactor.connectTCP(self._control_host, self._control_port,
                           #VServiceToPlatformTwistedClientFactory(self, cryptor=self._cryptor))
        
        ##
        ## run executor
        ##
        #reactor.listenTCP(self._bind_port, 
                          #VServiceTwistedConnFactory(self, self._cryptor),
                          #interface=self._interface)
        
        ##
        ## reactor run!
        ##
        #reactor.run()
    
    ##----------------------------------------------------------------------
    #def stop(self):
        #""""""
        #reactor.stop()
    
    ##
    ## properties
    ##
    #@property
    #def heartbeat(self):
        #""""""
        #return actions.Hearbeat(self.id)
    
    #@property
    #def id(self):
        #""""""
        #return self._id
    
    #@property
    #def welcome(self):
        #""""""
        #return actions.Welcome(self.id)

    ##
    ## op conn
    ##
    ##----------------------------------------------------------------------
    #def add_bind(self, cid, conn):
        #""""""
        #if not self._conn_pool.has_key(cid):
            #self._conn_pool[cid] = conn
        #else:
            #raise AssertionError('repeat client id for service:{}'.format(self.id))
    
    ##----------------------------------------------------------------------
    #def get_conn(self, cid):
        #""""""
        #return self._conn_pool.get(cid)
        
    
    ##----------------------------------------------------------------------
    #def get_task_status(self, task_id):
        #""""""
        #if self._task_map.has_key(task_id):
            #return actions.TaskStatus(task_id, state=client.TASK_STATE_PENDING)
        #else:
            #return None
        
    ##----------------------------------------------------------------------
    #def get_task_ack(self, task_id):
        #""""""
        #if task_id in self._task_pool.keys():
            #return actions.TaskACK(task_id)
        #else:
            #return None