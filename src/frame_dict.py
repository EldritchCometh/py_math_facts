import tkinter as tk
import re
import random


class FrameDict:


    def __init__(self, parent, colors = False):
        
        self._frames = {'frame': parent}
        self._colors = colors


    def _validate_path(self, path):
        
        err_suffix = \
            "empty or in the sequence of one or more " \
            "'v' or 'h' followed by a positive integer, " \
            "separated by '/' (e.g., '' or 'v3/h2/h4/v1')"
        if not isinstance(path, str):
            raise TypeError(f"Key must be a string that is {err_suffix}")
        if path == '':
            return
        if not re.match(r'^((v|h)\d+)(\/(v|h)\d+)*$', path):
            raise ValueError(f"Key must be {err_suffix}")


    def _get_dict(self, frame_path):

        self._validate_path(frame_path)
        if frame_path == '':
            return self._frames
        current = self._frames
        for key in frame_path.split('/'):
            current = current[key]
        return current


    def v_split(self, frame_path, frame_classes, weights=None):

        if weights and len(weights) != len(frame_classes):
            err = "length of weights must match length of frame_classes"
            raise ValueError(err)
        weights = weights or [1] * len(frame_classes)
        parent_dict = self._get_dict(frame_path)
        parent_frame = parent_dict['frame']
        
        parent_frame.columnconfigure(0, weight=1)
        for i, fc in enumerate(frame_classes):
            parent_frame.rowconfigure(i, weight=weights[i])
            new_frame = fc(parent_frame)
            if self._colors:
                new_frame.config(bg=f'#{random.randint(0, 0xFFFFFF):06x}')
            parent_dict[f'v{str(i)}'] = {'frame': new_frame}
            new_frame.grid(row=i, column=0, sticky='nsew')

    
    def h_split(self, frame_path, frame_classes, weights=None):

        if weights and len(weights) != len(frame_classes):
            err = "length of weights must match length of frame_classes"
            raise ValueError(err)
        weights = weights or [1] * len(frame_classes)
        parent_dict = self._get_dict(frame_path)
        parent_frame = parent_dict['frame']
        
        parent_frame.rowconfigure(0, weight=1)
        for i, fc in enumerate(frame_classes):
            parent_frame.columnconfigure(i, weight=weights[i])
            new_frame = fc(parent_frame)
            if self._colors:
                new_frame.config(bg=f'#{random.randint(0, 0xFFFFFF):06x}')
            parent_dict[f'h{str(i)}'] = {'frame': new_frame}
            new_frame.grid(row=0, column=i, sticky='nsew')


    def get(self, frame_path):

        return self._get_dict(frame_path)['frame']
