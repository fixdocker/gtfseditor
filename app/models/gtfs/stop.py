#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from ..base import Base
from ..mixins import ToJSONMixin


class Stop(Base, ToJSONMixin):

    __tablename__ = 'stops'
    __versioned__ = {
        'base_classes': (Base, ToJSONMixin, )
    }

    stop_id = Column(types.Integer, primary_key=True)
    stop_code = Column(types.String(50))
    stop_desc = Column(types.String(250))
    stop_name = Column(types.String(250))
    stop_lat = Column(types.Float(precision=53))
    stop_lon = Column(types.Float(precision=53))
    stop_calle = Column(types.String(250))
    stop_numero = Column(types.String(50))
    stop_entre = Column(types.String(250))
    stop_esquina = Column(types.String(250))
