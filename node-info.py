#!/usr/bin/env python3

import math
import meshtastic
import meshtastic.tcp_interface
import json
import logging
import sys
import tkinter as tk

logger = logging.getLogger(__name__)
logging.basicConfig(filename='mesh-info.log', level=logging.INFO)
logger.info('Started')

def drawNodeInfo(parent, nodes_dict, node_num, iface):
    print(parent)
    print(node_num)
    if len(parent.winfo_children()) > 0:
        for widget in parent.winfo_children():
            widget.destroy()

    node_info = json.dumps(nodes_dict.get(node_num), indent=4)
    lbl_node = tk.Label(master=parent, text=node_info, justify="left")
    lbl_node.pack()

    btn_back = tk.Button(master=parent, text="Back", command=lambda: drawGrid(iface, parent))
    btn_back.pack()


def drawGrid(iface, parent):
    if len(parent.winfo_children()) > 0:
        for widget in parent.winfo_children():
            widget.destroy()
    nodes = iface.nodesByNum
    if nodes is None:
        logger.error("no nodes found")
        sys.exit(1)
    
    node_nums = list(nodes.keys())
    
    cols = 5
    rows = math.ceil(len(nodes) / cols)
    row = rows
    
    # Build node grid
    count = 0
    
    while row > 0:
        for i in range(cols):
            frame = tk.Frame(
                    master=parent,
                    relief=tk.RAISED,
                    borderwidth=1
            )
            frame.grid(row=rows-row, column=i)
            node_name = nodes.get(node_nums[count]).get('user').get('longName')
            node_num = node_nums[count]
            button = tk.Button(master=frame, text=node_name, command=lambda: drawNodeInfo(parent, nodes, node_num, iface))
            button.pack()
            count = count+1
    
        row = row -1
    



def main():
    my_node='192.168.1.105'
    
    # initialize connection to node
    iface = meshtastic.tcp_interface.TCPInterface(hostname=my_node)
    
    # Get node info for header
    myNode = iface.getMyNodeInfo()
    if myNode is None:
        logger.error('no node data received')
        sys.exit(1)
    
    window = tk.Tk()
    logger.info('window initialized')
    
    # Build header
    longName = myNode.get('user').get('longName')
    battery = myNode.get('deviceMetrics').get('batteryLevel')
    
    header_frame = tk.Frame(master=window, height=10)
    header_text = tk.Label(master=header_frame, text=f"{longName} - Battery: {battery}%")
    header_frame.pack(fill=tk.X)
    header_text.pack()

    main_frame = tk.Frame()
    if len(main_frame.winfo_children()) == 0:
        drawGrid(iface, main_frame) 
    main_frame.pack()


    
    btn_refresh = tk.Button(master=window, text="Refresh", command=lambda: drawGrid(iface, main_frame))
    btn_refresh.pack()
    btn_close = tk.Button(master=window, text='Close', command=lambda: window.quit())
    btn_close.pack()
    
    
    
    tk.mainloop()


if __name__ == "__main__":
    main()
