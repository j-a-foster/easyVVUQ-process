"""Custom decoder for Process's mfiles.

Extracts data from Process's mfiles for easyVVUQ to use.
"""

import easyvvuq as uq
import numpy as np
from typing import Dict, Any, Optional
from process.io.mfile import MFile
import regex as re
from pathlib import Path


class MfileDecoder(uq.decoders.JSONDecoder):
    """Interprets Process's mfiles to extract repsonses for easyVVUQ.

    Subclasses easyVVUQ's JSON decoder.
    """

    def _get_raw_data(self, out_path: str) -> Dict:
        """Parse mfile and return dictionary of all output data.

        Parameters
        ----------
        out_path : str
            Path to mfile

        Returns
        -------
        Dict
            All output data contained in mfile
        """
        mfile = MFile(Path(out_path))
        mfile_dict = {}
        for param_name in mfile.data:
            param_value = mfile.data[param_name].get_scan(-1)
            mfile_dict[param_name] = param_value

        return mfile_dict

    def _process_raw_data(self, raw_data: Dict[str, Any]) -> Dict[str, float]:
        """Perform any required processing of raw mfile data dict.

        May include filtering for desired responses.

        Parameters
        ----------
        raw_data : Dict[str, Any]
            Entire raw output dictionary

        Returns
        -------
        Dict[str, float]
            Processed output dictionary
        """
        # Add objective function to responses dict
        responses = {"concost": raw_data["concost"], "cdirt": raw_data["cdirt"]}

        return responses

    def parse_sim_output(self, run_info: Optional[Dict] = None) -> Dict[str, float]:
        """Parse mfile, process it and return dict to easyVVUQ.

        Adapted from JSON decoder source to include _process_raw_data() step.

        Parameters
        ----------
        run_info : Optional[Dict], optional
            Run information supplied by easyVVUQ, by default None

        Returns
        -------
        Dict[str, float]
            Response data for easyVVUQ

        Raises
        ------
        RuntimeError
            Raised if field is absent from processed output data
        """
        if run_info is None:
            run_info = {}

        def get_value(data, path):
            for node in path:
                data = data[node]
            return data

        out_path = self._get_output_path(run_info, self.target_filename)
        raw_data = self._get_raw_data(out_path)

        # Perform any required processing of raw data
        processed_data = self._process_raw_data(raw_data)

        data = []
        for col in self.output_columns:
            try:
                if isinstance(col, str):
                    data.append((col, processed_data[col]))
                elif isinstance(col, list):
                    data.append((".".join(col), get_value(processed_data, col)))
            except KeyError:
                raise RuntimeError("no such field: {} in this mfile".format(col))
        return dict(data)
