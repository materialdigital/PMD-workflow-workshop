{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# First steps through pyiron"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This section gives a brief introduction about fundamental concepts of pyiron and how they can be used to setup, run and analyze atomic simulations. As a first step we import the libraries [numpy](http://www.numpy.org/) for data analysis and [matplotlib](https://matplotlib.org/) for visualization."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "%matplotlib inline\n",
    "import matplotlib.pylab as plt"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To import pyiron simply use:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2018-02-09T18:45:45.068257Z",
     "start_time": "2018-02-09T18:45:43.533004Z"
    }
   },
   "outputs": [],
   "source": [
    "from pyiron_atomistics import Project"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The Project object introduced below is central in pyiron. It allows to name the project as well as to derive all other objects such as structures, jobs etc. without having to import them. Thus, by code completion *Tab* the respective commands can be found easily."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We now create a pyiron Project named 'first_steps'."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "pr = Project(path='first_steps')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The project name also applies for the directory that is created for the project."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Perform a LAMMPS MD simulation"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Having created an instance of the pyiron Project we now perform a [LAMMPS](http://lammps.sandia.gov/) molecular dynamics simulation."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "For this basic simulation example we construct an fcc Al crystal in a cubic supercell (`cubic=True`). For more details on generating structures, please have a look at our [structures example](./structures.ipynb)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "1296530f94ae4dbb834f32e2150d93bb",
       "version_major": 2,
       "version_minor": 0
      },
      "text/html": [
       "<p>Failed to display Jupyter Widget of type <code>NGLWidget</code>.</p>\n",
       "<p>\n",
       "  If you're reading this message in the Jupyter Notebook or JupyterLab Notebook, it may mean\n",
       "  that the widgets JavaScript is still loading. If this message persists, it\n",
       "  likely means that the widgets JavaScript library is either not installed or\n",
       "  not enabled. See the <a href=\"https://ipywidgets.readthedocs.io/en/stable/user_install.html\">Jupyter\n",
       "  Widgets Documentation</a> for setup instructions.\n",
       "</p>\n",
       "<p>\n",
       "  If you're reading this message in another frontend (for example, a static\n",
       "  rendering on GitHub or <a href=\"https://nbviewer.jupyter.org/\">NBViewer</a>),\n",
       "  it may mean that your frontend doesn't currently support widgets.\n",
       "</p>\n"
      ],
      "text/plain": [
       "NGLWidget()"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "basis = pr.create_ase_bulk('Al', cubic=True)\n",
    "supercell_3x3x3 = basis.repeat([3, 3, 3])\n",
    "supercell_3x3x3.plot3d()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Here `create_ase_bulk` uses the [ASE bulk module](https://wiki.fysik.dtu.dk/ase/ase/build/build.html). The structure can be modified - here we extend the original cell to a 3x3x3 supercell (`repeat([3, 3, 3]`). Finally, we plot the structure using [NGlview](http://nglviewer.org/nglview/latest/api.html)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The project object allows to create various simulation job types. Here, we create a LAMMPS job."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "job = pr.create_job(job_type=pr.job_type.Lammps, job_name='Al_T800K')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Further, we specify a Molecular Dynamics simulation at $T=800$ K using the supercell structure created above."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2018-02-09T18:45:46.155546Z",
     "start_time": "2018-02-09T18:45:45.553946Z"
    }
   },
   "outputs": [],
   "source": [
    "job.structure = supercell_3x3x3\n",
    "job.calc_md(temperature=800, pressure=0, n_ionic_steps=10000)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To see all available interatomic potentials which are compatible with the structure (for our example they must contain Al) and the job type (here LAMMPS) we call `job.list_potentials()`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['Al_Mg_Mendelev_eam', 'Zope_Ti_Al_2003_eam', 'Al_H_Ni_Angelo_eam']"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "job.list_potentials()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "From the above let us select the first potential in the list."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2018-02-09T18:45:46.735000Z",
     "start_time": "2018-02-09T18:45:46.202421Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Selected potential:  Al_Mg_Mendelev_eam\n"
     ]
    }
   ],
   "source": [
    "pot = job.list_potentials()[0]\n",
    "print ('Selected potential: ', pot)\n",
    "job.potential = pot"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To run the LAMMPS simulation (locally) we now simply use:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "job.run()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Analyze the calculation"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "After the simulation has finished the information about the job can be accessed through the Project object."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2018-02-09T18:45:47.358552Z",
     "start_time": "2018-02-09T18:45:46.757140Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'groups': ['input', 'output'], 'nodes': ['NAME', 'server', 'VERSION', 'TYPE']}"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "job = pr['Al_T800K']\n",
    "job"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Printing the job object (note that in Jupyter we don't have to call a print statement if the variable/object is in the last line). The output lists the variables (nodes) and the directories (groups). To get a list of all variables stored in the generic output we type:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2018-02-09T18:45:47.421055Z",
     "start_time": "2018-02-09T18:45:47.374180Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'groups': [], 'nodes': ['temperatures', 'positions', 'steps', 'forces', 'energy_pot', 'energy_tot', 'volume', 'cells', 'pressures', 'unwrapped_positions', 'time']}"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "job['output/generic']"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "An animated 3d plot of the MD trajectories is created by:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2018-02-09T18:45:47.536944Z",
     "start_time": "2018-02-09T18:45:47.421055Z"
    }
   },
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "8b809c517e50423f81fb574ebd6eb06f",
       "version_major": 2,
       "version_minor": 0
      },
      "text/html": [
       "<p>Failed to display Jupyter Widget of type <code>NGLWidget</code>.</p>\n",
       "<p>\n",
       "  If you're reading this message in the Jupyter Notebook or JupyterLab Notebook, it may mean\n",
       "  that the widgets JavaScript is still loading. If this message persists, it\n",
       "  likely means that the widgets JavaScript library is either not installed or\n",
       "  not enabled. See the <a href=\"https://ipywidgets.readthedocs.io/en/stable/user_install.html\">Jupyter\n",
       "  Widgets Documentation</a> for setup instructions.\n",
       "</p>\n",
       "<p>\n",
       "  If you're reading this message in another frontend (for example, a static\n",
       "  rendering on GitHub or <a href=\"https://nbviewer.jupyter.org/\">NBViewer</a>),\n",
       "  it may mean that your frontend doesn't currently support widgets.\n",
       "</p>\n"
      ],
      "text/plain": [
       "NGLWidget(count=101)"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "job.animate_structure()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To analyze the temperature evolution we plot it as function of the MD step."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x2b0b61ac8e80>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "temperatures = job['output/generic/temperature']\n",
    "steps = job['output/generic/steps']\n",
    "plt.plot(steps, temperatures)\n",
    "plt.xlabel('MD step')\n",
    "plt.ylabel('Temperature [K]');"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "In the same way we can plot the trajectories."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x2b0b621e0ac8>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "pos = job['output/generic/positions']\n",
    "x, y, z = [pos[:, :, i] for i in range(3)]\n",
    "sel = np.abs(z) < 0.1\n",
    "fig, axs = plt.subplots(1,1)\n",
    "axs.scatter(x[sel], y[sel])\n",
    "axs.set_xlabel('x [$\\AA$]')\n",
    "axs.set_ylabel('y [$\\AA$]')\n",
    "axs.set_aspect('equal', 'box');"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Perform a series of jobs"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To run the MD simulation for various temperatures we can simply loop over the desired temperature values."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "for temperature in np.arange(200, 1200, 200):\n",
    "    job = pr.create_job(pr.job_type.Lammps, \n",
    "                        'Al_T{}K'.format(int(temperature)))\n",
    "    job.structure = supercell_3x3x3\n",
    "    job.potential = pot     \n",
    "    job.calc_md(temperature=temperature, \n",
    "                pressure=0, \n",
    "                n_ionic_steps=10000)\n",
    "    job.run()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To inspect the list of jobs in our current project we type (note that the existing job from the previous excercise at $T=800$ K has been recognized and not run again):"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['Al_T600K', 'Al_T800K', 'Al_T1000K', 'Al_T200K', 'Al_T400K']"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pr"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can now iterate over the jobs and extract volume and mean temperature."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "vol_lst, temp_lst = [], []\n",
    "for job in pr.iter_jobs(convert_to_object=False):\n",
    "    volumes = job['output/generic/volume']\n",
    "    temperatures = job['output/generic/temperature']\n",
    "    temp_lst.append(np.mean(temperatures[:-20]))\n",
    "    vol_lst.append(np.mean(volumes[:-20]))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Then we can use the extracted information to plot the thermal expansion, calculated within the $NPT$ ensemble. For plotting the temperature values in ascending order the volume list is mapped to the sorted temperature list."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x2b0b6289f710>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure()\n",
    "vol_lst[:] = [vol_lst[np.argsort(temp_lst)[k]] \n",
    "              for k in range(len(vol_lst))]\n",
    "plt.plot(sorted(temp_lst), vol_lst, \n",
    "         linestyle='-',marker='o',)\n",
    "plt.title('Thermal expansion')\n",
    "plt.xlabel('Temperature [K]')\n",
    "plt.ylabel('Volume [$\\AA^3$]');"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Create a series of projects"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We extend the previous example and compute the thermal expansion for three of the available aluminum potentials. First, let us create a new pyiron project named 'Al_potentials'. We can use the information of the previously run job 'Al_T200K' of the 'first_steps' project to find all the compatible potentials."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "pr = Project('Al_potentials')\n",
    "pot_lst = pr['../first_steps/Al_T200K'].load_object().list_potentials()[:3]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['Al_Mg_Mendelev_eam', 'Zope_Ti_Al_2003_eam', 'Al_H_Ni_Angelo_eam']"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pot_lst"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Note again that `list_potentials()` automatically only returns the potentials that are compatible with the structure (chemical species) and the job type."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can now loop over the selected potentials and run the MD simulation for the desired temperature values for any of the potentials."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Interatomic potential used:  Al_Mg_Mendelev_eam\n",
      "Interatomic potential used:  Zope_Ti_Al_2003_eam\n",
      "Interatomic potential used:  Al_H_Ni_Angelo_eam\n"
     ]
    }
   ],
   "source": [
    "for pot in pot_lst:\n",
    "    print ('Interatomic potential used: ',pot)\n",
    "    pr_pot = pr.create_group(pot)\n",
    "    for temperature in np.arange(200, 1200, 200):\n",
    "        job = pr_pot.create_job(pr.job_type.Lammps, \n",
    "                                'Al_T{}K'.format(int(temperature)))\n",
    "        job.structure = supercell_3x3x3\n",
    "        job.potential = pot                \n",
    "        job.calc_md(temperature=temperature, \n",
    "                    pressure=0, \n",
    "                    n_ionic_steps=10000)\n",
    "        job.run()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "With the `pr.create_group()` command a new subproject (directory) is created named here by the name of the potential. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "For any particular potential the thermal expansion data can be obtained again by looping over the jobs performed using that potential. To obtain the thermal expansion curves for all the potentials used we can simply iterate over the subprojects (directories) created above by using the `pr.iter_groups()` command."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x2b0b628e8be0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "for p in pr.iter_groups():\n",
    "    vol_lst, temp_lst = [], []\n",
    "    for out in p.iter_jobs(path='output/generic'):\n",
    "        volumes = out['volume']\n",
    "        temperatures = out['temperature']\n",
    "        temp_lst.append(np.mean(temperatures[:-20]))\n",
    "        vol_lst.append(np.mean(volumes[:-20]))\n",
    "    # Plot only if there is a job in that group\n",
    "    if len(p.get_job_ids()) > 0:\n",
    "        plt.plot(temp_lst, vol_lst, \n",
    "                 linestyle='-',marker='o',\n",
    "                 label=p.name) \n",
    "plt.legend(loc='best')    \n",
    "plt.title('Thermal expansion for different interatomic potentials')\n",
    "plt.xlabel('Temperature [K]')\n",
    "plt.ylabel('Volume [$\\AA^3$]');"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "anaconda-cloud": {},
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.7"
  },
  "latex_envs": {
   "LaTeX_envs_menu_present": true,
   "autocomplete": true,
   "bibliofile": "biblio.bib",
   "cite_by": "apalike",
   "current_citInitial": 1,
   "eqLabelWithNumbers": true,
   "eqNumInitial": 1,
   "hotkeys": {
    "equation": "Ctrl-E",
    "itemize": "Ctrl-I"
   },
   "labels_anchors": false,
   "latex_user_defs": false,
   "report_style_numbering": false,
   "user_envs_cfg": false
  },
  "toc": {
   "nav_menu": {
    "height": "122px",
    "width": "252px"
   },
   "number_sections": true,
   "sideBar": true,
   "skip_h1_title": false,
   "toc_cell": false,
   "toc_position": {},
   "toc_section_display": "block",
   "toc_window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}