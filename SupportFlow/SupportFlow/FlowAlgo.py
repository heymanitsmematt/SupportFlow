from app.models import *

#request, DetailView?
class Flow(object):
    def __init__(self):
        self.template_name = 'app/flow.html'
        self.software = Parent.objects.get(id = 1) #software_id param when class view

        self.node_1_raw = Node_1.objects.all()
        self.node_2_raw = Node_2.objects.all()
        self.node_3_raw = Node_3.objects.all()
   
        self.node_3_json = []
        self.node_2_json = []
        self.node_1_json = []

        i=0

    def flow(self):

        for node in self.node_3_raw:
            self.node_3_json.append({'name' : node.node_name})
           
        
        for node2 in self.node_2_raw:
            if node2.node_3_set.count > 0:
                self.node_2_json.append({'name': node2.node_name, 'children' : ''})
            else:
                self.node_2_json.append({'name' : node2.node_name})

        for node2 in self.node_2_raw:
            if node2.node_3_set.count > 0:
                self.node_2_json.append({'name': node2.node_name, 'children' : ''})
            else:
                self.node_2_json.append({'name' : node2.node_name})

        #create main json object
        self.json = [{'name' : self.software.parent_name, 'children' : ''}]
        
        #add node_1 to parrent
        # eventual last step self.json['children'] = self.json_node_1
        i=0
        
        for node1 in self.node_1_json:
            self.this_node1_json = []
            try:
                self.this_node = Node_1.objects.get(node_name__contains = self.node_1_json[i]['name'])
                self.this_node_set = self.this.node_node_2_set.all()
                #self.this_set_json = [] maybe move to beginning to ensure it's cleared every time? - moved
                if len(self.this_node_set) > 0:
                    for n in self.this_node_set:
                        self.this_set_json.append({'name' : n.node_name})
                        self.node_1_json[i].append({'children' : self.this_set_json})
                        i += 1
            except:
                i +=1 
                pass
    



        

    return render_to_response(template_name, {'software' : software, 'parent_child_set' : parent_child_set, 
                                              'node_1_child_set' : node_1_child_set, 'node_2_list' : node_2_list },
                              context_instance = RequestContext(request))


def flow(request, software_id):
    
    template_name = 'app/flow.html'
    software = Parent.objects.get(id = software_id)
    
    node_1_raw = Node_1.objects.all()
    node_2_raw = Node_2.objects.all()
    node_3_raw = Node_3.objects.all()
   
    node_3_json = []
    node_2_json = []
    node_1_json = []
    
    for node in node_3_raw:
        node_3_json.append({'name' : node.node_name})

    for node in node_2_raw:
        node_2_json.append({'name' : node.node_name})

    for node in node_1_raw:
        node_1_json.append({'name' : node.node_name})

    json = [{'name' : software.parent_name, 'children' : ''}]
    
    i=0
    
    for node in node_1_json:
        try:
            this_node = Node_1.objects.get(node_name__contains = node_1_json[i]['name'])
            this_node_set = this.node.node_2_set.all()
            this_set_json = []
            if len(this_node_set) > 0:
                for n in this_node_set:
                    this_set_json.append({'name' : n.node_name})
                    node_1_json[i].append({'children' : this_set_json})
                    i += 1
        except:
            i +=1 
            pass

    '''
    '''
    for node in node_2_json:
        try:
            this_node = Node_2.objects.get(node_name__contains = node_2_json[i]['name'])
            this_node_set = this_node.node_3_set.all()
            this_set_json  = []
            if len(this_node_set) > 0:
                for n in this_node_set:
                    this_set_json.append({'name' : n.node_name})
                    node_2_json[i]['children'] = this_set_json
                    i += 1
            else : 
                i += 1
                pass
        except: 
            i += 1
            pass
            
    



        f.json.append({'name' : n1.node_name, 'children' : [{'name' : n2.node_name, 'children' : [{'name' : n3.node_name}]}]})