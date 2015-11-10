#!/bin/bash
 
find  Protection RedList BDTFX/bin Catminat/bin Flores wxflore-x.x  bin -type f -ctime -5 | tar cvfz toto.tgz  -T -

