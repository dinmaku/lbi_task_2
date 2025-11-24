<template>
   <div class="min-h-screen bg-gray-100 py-10 px-12 overflow-y-auto">
    <div class="flex flex-col">
       <div class="mt-6 items-start text-start">
           <p class="text-2xl font-bold ">Hi, {{ Name }}</p>
           <p class="text-lg font-semibold tracking-wide text-blue-400">Get ready to achieve more today.</p>
       </div>
       <div class = "mt-7 bg-blue-100 w-3/4 h-[250px] rounded-xl shadow-sm">
          <div class="m-auto p-3 flex justify-between items-center">
             <div class="flex flex-col text-left space-y-3">
                <p class="font-bold tracking-wide text-4xl text-blue-900">Your Projects</p>
                <p class="font-seimibold tracking-light text-xl text-blue-400">Check your latest projects and schedules</p>
                <button @click="showAddNewProject" class="mt-5 px-2 py-3 bg-blue-500 text-gray-100 rounded-lg font-semibold cursor-pointer transition-transform duration-300 transform hover:scale-105">+ Add New Project</button>
             </div>
              <img src="../assets/icons/office.png" class="mr-20 w-1/5 h-auto" alt="">
          </div>
       </div>
 
       <div class="flex flex-row justify-start">
          <div class="grid grid-cols-4 mt-10 space-y-5 gap-x-6 items-stretch">
            
            <div
              v-for="project in projects"
              :key="project.project_id"
              class="w-[390px] h-auto bg-blue-50 border border-gray-300 rounded-xl shadow-md p-5 transition-transform duration-300 transform hover:scale-105 cursor-pointer space-y-5"
              @click="showProjectDetails(project.project_id)"
            >

              <h2 class="text-lg font-semibold text-gray-400 text-start">
                {{ project.start_date ? project.start_date.substring(0,10) : 'No Start Date' }}
              </h2>

              <div class="flex justify-between items-center">
                <div class="flex flex-col text-left">
                  <h2 class="text-2xl text-gray-700 font-semibold">{{ project.project_name }}</h2>

                  <p class="text-md text-blue-400">
                    Contains 
                    <span class="text-blue-600 font-semibold">
                      {{ project.tasks.length }}
                    </span>
                    task/s
                  </p>
                </div>

                <span class="px-2 py-1 text-xs rounded-full"
                  :class="statusClass(project.status)">
                  {{ project.status }}
                </span>
              </div>


              <div>
                <div class="w-full bg-gray-200 rounded-full h-3 ">
                  <div class="h-3 rounded-full"
                    :class="progressColor(project.status)"
                    :style="{ width: calculateProgress(project.tasks) + '%' }">
                  </div>

                  <div class="flex justify-between items-center font-semibold mt-1 text-gray-400">
                    <p>Progress</p>
                    <p class="text-gray-700">{{ calculateProgress(project.tasks) }}%</p>
                  </div>
                </div>
              </div>

              <hr class="my-12 border-gray-300" />

              <div class="flex justify-between items-center mt-9">
                <div class="flex flex-row gap-x-1">
                  <img src="../assets/icons/folder.png" class="w-6 h-6" alt="">

                  <button title="Add Task" @click="toggleExistingTask(project.project_id)"
                    class="w-6 h-6 flex items-center justify-center rounded-full text-xl text-white font-bold cursor-pointer"
                    :class="statusBg(project.status)">
                    <span class="mb-1">+</span>
                  </button>
                </div>


                <div class="py-1 px-2 flex items-center justify-center rounded-full text-sm text-white font-semibold"
                  :class="statusBg(project.status)">
                  <p>{{ daysLeft(project.end_date) }} days left</p>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>
  
      <form v-if="addProjectForm" @click.self="addProjectForm = false"
          class="fixed inset-0 bg-gray-800/20 overflow-y-auto flex justify-center items-center z-[99]">

          <div class="bg-white rounded-xl shadow-2xl w-full h-[850px] max-w-3xl mx-4 my-10 
                      flex flex-col md:flex-row overflow-hidden pb-5">

            <div class="flex flex-col text-start px-5 py-5 w-full">
              <h1 class="text-gray-700 font-bold text-3xl">New Project</h1>
              <span class="text-gray-500 font-semibold text-md italic mt-2">
                Fill out the details below to initialize a new project.
              </span>

             
              <div class="flex flex-col justify-start mt-10">
                <input v-model="newProject.project_name" type="text" class="w-full h-14 px-2 bg-gray-100 rounded-lg shadow-sm mt-5"
                  placeholder="Project Name">

                <textarea v-model="newProject.description" class="w-full h-22 px-2 py-2 bg-gray-100 rounded-lg shadow-sm mt-5"
                  placeholder="Description"></textarea>

                <label class="text-md font-semibold text-gray-600 mt-5">Deadline:</label>
                <input v-model="newProject.end_date" type="date" class="w-full h-14 bg-gray-100 rounded-lg shadow-sm px-3 cursor-pointer mt-2">

             
                <div class="flex flex-row items-center gap-x-2 mt-5">
                  <label class="text-lg font-semibold text-gray-600">Add task</label>
                  <button
                    @click="showAddTask"
                    type="button"
                    class="w-7 h-7 flex items-center justify-center rounded-full bg-blue-500 
                          transition transform duration-300 hover:scale-105 cursor-pointer">
                    <span class="mb-1 text-2xl text-white font-bold">+</span>
                  </button>
                </div>

      
                <div class="mt-5 bg-gray-50 border border-gray-200 rounded-lg p-4"
                  v-if="selectedTasks.length > 0">

                <h2 class="text-lg font-bold text-gray-700 mb-3">Tasks Added</h2>

                <div class="flex flex-col space-y-3 max-h-46 overflow-y-auto">

        
                  <div v-for="taskId in selectedTasks" :key="taskId"
                      class="flex items-center justify-between bg-white px-3 py-2 rounded-lg shadow-sm border">

                    <div class="flex flex-col">
                      <span class="font-semibold text-gray-800">
                        {{ getTaskById(taskId).title }}
                      </span>
                      <span class="text-sm text-gray-500 truncate block w-1/2">
                        {{ getTaskById(taskId).description }}
                      </span>
                    </div>

                    <button @click="removeTask(taskId)"
                            class="text-red-600 font-bold text-xl leading-none hover:text-red-800 cursor-pointer">
                      ×
                    </button>
                  </div>

                </div>
              </div>
             
              </div>
              <button 
               @click="submitNewProject"
               type="button"
               :disabled="isSubmitting"
              class="mt-10 bg-blue-500 px-3 py-2 rounded-lg shadow-sm cursor-pointer text-xl text-white font-semibold transition transform duration-300 hover:scale-103"
              > {{ isSubmitting ? "Creating..." : "Create Project" }}</button>
            </div>
            
          </div>
        </form>

        <div v-if="addTaskModal" 
            @click.self="addTaskModal = false"
            class="fixed inset-0 bg-gray-800/20 backdrop-blur-sm overflow-y-auto 
                    flex justify-center items-center z-[999]">

          <div class="bg-white w-full max-w-lg rounded-xl shadow-xl p-6 mx-4" @click.stop>

            <h1 class="text-2xl font-bold text-gray-700">Add Existing Task</h1>
            <p class="text-gray-500 text-sm mt-1">Select an existing task to attach to this project.</p>

            <!-- TASK LIST -->
            <div class="mt-6 max-h-64 overflow-y-auto space-y-3">
                <div
                  v-for="task in availableTasks"
                  :key="task.task_id"
                  class="flex items-center justify-between p-3 bg-gray-100 rounded-lg 
                        hover:bg-gray-200 cursor-pointer"
                  @click="toggleTask(task.task_id)"
                >

                  <div class="flex flex-col w-64 text-left">
                    <p class="font-semibold text-gray-800 truncate">{{ task.title }}</p>
                    <p class="text-sm text-gray-500 truncate">{{ task.description }}</p>
                  </div>

                  
                  <input 
                    type="checkbox"
                    :checked="selectedTasks.includes(task.task_id)"
                    @click.stop 
                    @change="toggleTask(task.task_id)"  
                    class="w-5 h-5 cursor-pointer"
                  />
                </div>
              </div>

         
             <div class="flex justify-end gap-x-3 mt-6">
              <button @click="addTaskModal = false"
                      class="px-5 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300">
                Done
              </button>
            </div>

          </div>
        </div>

      <!--Add Tasks to Existing Project-->
      <div v-if="addExistingTaskModal"
        @click.self="addExistingTaskModal = false"
        class="fixed inset-0 bg-gray-800/20 backdrop-blur-sm overflow-y-auto 
                flex justify-center items-center z-[999]">

      <div class="bg-white w-full max-w-lg rounded-xl shadow-xl p-6 mx-4" @click.stop>

        <h1 class="text-2xl font-bold text-gray-700">Assign Existing Task</h1>
        <p class="text-gray-500 text-sm mt-1">Choose one or more tasks to attach to this project.</p>

        <!-- EXISTING TASK LIST -->
        <div class="mt-6 max-h-64 overflow-y-auto space-y-3">
          <div
            v-for="task in availableTasksForProject"
            :key="task.task_id"
            class="flex items-center justify-between p-3 bg-gray-100 rounded-lg 
                  hover:bg-gray-200 cursor-pointer"
            @click="toggleTask(task.task_id)"
          >

            <div class="flex flex-col w-64 text-left">
              <p class="font-semibold text-gray-800 truncate">{{ task.title }}</p>
              <p class="text-sm text-gray-500 truncate">{{ task.description }}</p>
            </div>

            <input 
              type="checkbox"
              :checked="selectedTasks.includes(task.task_id)"
              @click.stop
              @change="toggleTask(task.task_id)"
              class="w-5 h-5 cursor-pointer"
            />
          </div>
        </div>

        <!-- BUTTONS -->
        <div class="flex justify-end gap-x-3 mt-6">
          <button @click="addExistingTaskModal = false"
                  class="px-5 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300">
            Cancel
          </button>

          <button @click="assignTasksToProject"
                  class="px-5 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 cursor-pointer">
            Save Changes
          </button>
        </div>

      </div>
    </div>
   
      <!--Project Details Modal--> 
      <div v-if="projectDetailsModal" @click.self="projectDetailsModal = false" class="fixed inset-0 bg-gray-800/20 overflow-y-auto flex justify-center items-center z-[99]"> 
          <div class="bg-white rounded-xl shadow-2xl w-full h-[850px] max-w-3xl mx-4 my-10 
                      flex flex-col md:flex-row overflow-hidden pb-5">

            <div class="flex flex-col text-start px-5 py-5 w-full">
              <h1 class="text-gray-700 font-bold text-3xl">Edit Project</h1>
              <span class="text-gray-500 font-semibold text-md italic mt-2">
                Update the details below to modify the existing project.
              </span>

             
              <div class="flex flex-col justify-start mt-10">
                 <div class="flex justify-start items-center gap-3">
                            <div
                              class="flex items-center gap-2 cursor-pointer hover:bg-gray-100 px-2 py-1 rounded-md transition"
                              @click="openStatusModal"
                            >
                              <span
                                class="w-3 h-3 rounded-full"
                                :class="{
                                  'bg-blue-500': selectedProject.status === 'In Progress',
                                  'bg-yellow-500': selectedProject.status === 'For QA',
                                  'bg-green-500': selectedProject.status === 'Done',
                                  'bg-purple-500': selectedProject.status === 'In Production',
                                  'bg-orange-500': selectedProject.status === 'Draft',
                                  'bg-red-500': selectedProject.status === 'Cancelled'
                                }"
                              ></span>
                              <span class="text-gray-800 font-medium capitalize">
                                {{ selectedProject.status }}
                              </span>
                            </div>
                          </div>


                <input v-model="selectedProject.project_name" type="text" class="w-full h-14 px-2 bg-gray-100 rounded-lg shadow-sm mt-5"
                  placeholder="Project Name">

                <textarea v-model="selectedProject.description" class="w-full h-22 px-2 py-2 bg-gray-100 rounded-lg shadow-sm mt-5"
                  placeholder="Description"></textarea>

                <label class="text-md font-semibold text-gray-600 mt-5">Deadline:</label>
                <input v-model="selectedProject.end_date" type="date" class="w-full h-14 bg-gray-100 rounded-lg shadow-sm px-3 cursor-pointer mt-2">

             
                <div class="flex flex-row items-center gap-x-2 mt-5">
                  <label class="text-lg font-semibold text-gray-600">Edit task</label>
                  <button
                    @click="toggleExistingTask(selectedProject.project_id)"
                    type="button"
                    class="w-7 h-7 flex items-center justify-center rounded-full bg-blue-500 
                          transition transform duration-300 hover:scale-105 cursor-pointer">
                    <span class="mb-1 text-2xl text-white font-bold">+</span>
                  </button>
                </div>

      
                <div class="mt-5 bg-gray-50 border border-gray-200 rounded-lg p-4"
                  v-if="selectedTasks.length > 0">

                <h2 class="text-lg font-bold text-gray-700 mb-3">Tasks Added</h2>

                <div class="flex flex-col space-y-3 max-h-46 overflow-y-auto">

        
                  <div v-for="taskId in selectedTasks" :key="taskId"
                      class="flex items-center justify-between bg-white px-3 py-2 rounded-lg shadow-sm border">

                    <div class="flex flex-col">
                      <span class="font-semibold text-gray-800">
                        {{ getTaskById(taskId).title }}
                      </span>
                      <span class="text-sm text-gray-500 truncate block w-100">
                        {{ getTaskById(taskId).description }}
                      </span>
                    </div>
                  </div>

                </div>
              </div>
             
              </div>
              <button 
               @click="updateProject"
               type="button"
               :disabled="isSubmitting"
              class="mt-10 bg-blue-500 px-3 py-2 rounded-lg shadow-sm cursor-pointer text-xl text-white font-semibold transition transform duration-300 hover:scale-103"
              > {{ isSubmitting ? "Saving..." : "Save" }}</button>
            </div>
                
          </div>
      </div>

      
      <div
      v-if="showStatusModal"
      @click.self="showStatusModal = false"
      class="fixed inset-0 bg-gray-800/40 flex justify-center items-center z-999"
    >
      <div class="bg-white rounded-lg shadow-lg w-[350px] p-6 space-y-5">
        <h2 class="text-xl font-semibold text-gray-800">Change Status</h2>

        <div class="space-y-2">
          <label
            v-for="option in statusOptions"
            :key="option"
            class="flex items-center space-x-2 cursor-pointer hover:bg-gray-100 p-2 rounded-md"
          >
            <input
              type="radio"
              name="status"
              :value="option"
              v-model="selectedStatus"
              class="text-blue-600 focus:ring-blue-500 cursor-pointer"
            />
            <span class="capitalize text-gray-700">{{ option }}</span>
          </label>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            @click="showStatusModal = false"
            class="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 transition cursor-pointer"
          >
            Cancel
          </button>
          <button
            @click="updateStatus"
            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition cursor-pointer"
          >
            Save
          </button>
        </div>
      </div>
    
    </div>




      <!-- Alert Modal -->
          <div v-if="showAlert" class="fixed inset-0 bg-gray-800/20 overflow-y-auto flex justify-center items-center z-999">
            <div :class="['bg-white p-5 rounded-lg shadow-lg w-[400px] border-l-4', alertType === 'success' ? 'border-green-500' : 'border-red-500']">
              <div class="flex justify-between items-center mb-4">
                <h3 :class="['text-lg font-semibold', alertType === 'success' ? 'text-green-600' : 'text-red-600']">
                  {{ alertType === 'success' ? 'Success' : 'Error' }}
                </h3>
              </div>
              <p class="text-gray-700">{{ alertMessage }}</p>
              <div class="flex justify-end mt-4">
                <button @click="closeAlert" class="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 cursor-pointer">
                  Close
                </button>
              </div>
            </div>
          </div>

   </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Projects",

 data() {
    return {
      baseURL: 'http://127.0.0.1:5000',
      projects: [],
      project: null,
      addProjectForm: false,
      addTaskModal: false,
      tasks: [],
      selectedTasks: [],
      newProject: {
          project_name: '',
          description: '',
          start_date: '',  
          end_date: '',
          status: 'In Progress'  
        },
      isSubmitting: false,
      showAlert: false,
      alertMessage: '',
      addExistingTaskModal: false, 
      selectedProjectId: null,
      selectedProject: 
        {
          project_id: null,
          project_name: '',
          description: '',
          start_date: '',
          end_date: '',
          status: '',
          tasks: []
        },
      projectDetailsModal: false,
      showStatusModal: false,
      statusOptions: ['Pending', 'In Progress', 'For QA', 'In Production', 'Completed', 'Draft', 'Cancelled'],

    };


  },

  methods: {
        showAlertMessage(type, message) {
          this.alertType = type;
          this.alertMessage = message;
          this.showAlert = true;
        },
        closeAlert() {
          this.showAlert = false;
          this.alertMessage = '';
          this.alertType = '';
        },

     statusClass(status) {
        switch(status) {
          case "Draft":
            return "bg-gray-300 text-gray-800";
          case "In Progress":
             return "bg-blue-300 text-blue-800";
          case "For QA":
             return "bg-yellow-300 text-yellow-800";
          case "In Production":
             return "bg-purple-300 text-purple-800";
          case "Completed":
             return "bg-green-300 text-green-800";
          default:
             return "bg-gray-200 text-gray-700"
        }
     },


    progressColor(status) {
        switch(status) {
          case "Draft":
          return "bg-gray-400";
        case "In Progress":
          return "bg-blue-500";
        case "For QA":
          return "bg-yellow-500";
        case "In Production":
          return "bg-purple-500";
        case "Done":
          return "bg-green-500";
        default:
          return "bg-gray-300";
        }
    },
    
     statusBg(status) {
        switch (status) {
          case "Draft": return "bg-gray-400";
          case "In Progress": return "bg-blue-500";
          case "For QA": return "bg-yellow-500";
          case "In Production": return "bg-purple-500";
          case "Complete": return "bg-green-500";
          default: return "bg-gray-300";
        }
      },
        showAddNewProject() {
          this.addProjectForm = true;
        },
        showAddTask() {
          this.addTaskModal = true;
        },
        showProjectDetails(projectId)
            {
              const found = this.projects.find(p => p.project_id === projectId);

              if (!found) {
                console.error("Project not found");
                return;
              }
              const cleanDate = found.end_date ? found.end_date.split('T')[0] : '';
              this.selectedProject = {
                ...found,
                end_date: cleanDate
              };
        
              this.selectedTasks = found.tasks?.map(t => t.task_id) || [];

              this.projectDetailsModal = true;
            },

        async fetchTasks() {
              try {
                const token = sessionStorage.getItem('access_token');
                if (!token) {
                  console.error('No token found');
                  this.$router.push('/');
                  return;
                }

                const response = await axios.get(`${this.baseURL}/fetch_tasks`, {
                  headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'
                  }
                });

                if (response.status === 200 && Array.isArray(response.data)) {
                  this.tasks = response.data;
                  console.log('Tasks fetched:', this.tasks);
                } else {
                  console.warn('Unexpected response format:', response);
                  this.tasks = [];
                }

              } catch (error) {
                console.error('Error fetching tasks:', error);
                this.tasks = [];
                this.showAlertMessage?.('error', 'Failed to load tasks. Please try again.');
              }
            },

      async submitNewProject() {
            if (!this.newProject.project_name) {
              this.showAlertMessage("error", "Project name is required!");
              return;
            }
             const userType = localStorage.getItem('user_type');

              if (userType === 'staff') {
                this.showAlertMessage('error', 'You are not authorized to create a project.');
                return;
              }
            const payload = {
              ...this.newProject,
              start_date: new Date().toISOString(),
              status: "In Progress",
              tasks: this.selectedTasks, 
            };

            this.isSubmitting = true;

            

            try {
              const token = sessionStorage.getItem('access_token');
              const response = await axios.post(`${this.baseURL}/projects/create`, payload, {
                headers: {
                  Authorization: `Bearer ${token}`,
                  'Content-Type': 'application/json'
                }
              });

              if (response.status === 201) {
                this.showAlertMessage("success", response.data.message);
                this.projects.push(response.data.project);
                this.addProjectForm = false;
                this.newProject = { project_name: '', description: '', end_date: '', status: 'In Progress' };
                this.selectedTasks = [];
              }
            } catch (error) {
              console.error("Error creating project:", error);
              this.showAlertMessage("error", "Failed to create project. See console for details.");
            } finally {
              this.isSubmitting = false;
            }
          },


          getTaskById(id) {
            return this.tasks.find(task => task.task_id === id) || {};
          },

        removeTask(taskId) {
          this.selectedTasks = this.selectedTasks.filter(id => id !== taskId);
        },

      toggleTask(id) {
          if (!id) return;

          const index = this.selectedTasks.indexOf(id);

          if (index === -1) {
            this.selectedTasks.push(id);
          } else {
            this.selectedTasks.splice(index, 1);
          }
        },

       async fetchProjects() {
          try {
            const userType = localStorage.getItem("user_type");
            const userId = sessionStorage.getItem("user_id");

            const response = await axios.get("http://localhost:5000/projects", {
              params: {
                user_type: userType,
                user_id: userId
              }
            });

            this.projects = response.data;
            console.log("Projects loaded:", this.projects);
          } catch (error) {
            console.error("Error loading projects:", error);
          }
        },

        calculateProgress(tasks) {
            if (!tasks.length) return 0;
            const completed = tasks.filter(t => t.status === "Done").length;
            return Math.round((completed / tasks.length) * 100);
          },

          daysLeft(endDate) {
            if (!endDate) return "—";
            const today = new Date();
            const deadline = new Date(endDate);
            const diff = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));
            return diff > 0 ? diff : 0;
          },

         async assignTasksToProject() {
          const userType = localStorage.getItem('user_type');

              if (userType === 'staff') {
                this.showAlertMessage('error', 'You are not authorized to add a task to project.');
                return;
              }
            if (!this.currentProjectId) return console.error("No project selected");
            

            try {
                const response = await axios.put("http://localhost:5000/tasks/assign-multiple", {
                  project_id: this.currentProjectId,
                  task_ids: this.selectedTasks
                });

                await this.fetchProjects();
                await this.fetchTasks();
                this.addExistingTaskModal = false;

                this.showAlertMessage("success", "Tasks assigned successfully!");
              } catch (err) {
                console.error("Assign error:", err);
                this.showAlertMessage("error", "Error assigning tasks:");
              }
          },

        toggleExistingTask(projectId) {
          this.addExistingTaskModal = true;
          this.currentProjectId = projectId;

          const project = this.projects.find(p => p.project_id === projectId);

          if (project) {
            console.log("Project data:", project);
            this.selectedTasks = project.tasks.map(t => t.task_id);

            console.log("Preselected tasks:", this.selectedTasks);
          } else {
            console.warn("Project not found in projects array");
          }
        },

        toggleTask(taskId) {
          if (this.selectedTasks.includes(taskId)) {
            this.selectedTasks = this.selectedTasks.filter(id => id !== taskId);
          } else {
            this.selectedTasks.push(taskId);
          }
        },

        openStatusModal() {
          this.showStatusModal = true;
          this.selectedStatus = this.selectedProject.status;
        },

        async updateStatus() {
          const userType = localStorage.getItem('user_type');

              if (userType === 'staff') {
                this.showAlertMessage('error', 'You are not authorized to change the status of the project.');
                return;
              }

          try {
            const response = await fetch(`http://localhost:5000/edit_project/${this.selectedProject.project_id}`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ status: this.selectedStatus }),
            });

            const result = await response.json();

            if (!response.ok) {
              throw new Error(result.error || 'Failed to update status');
            }

            // ✅ Update UI instantly
            this.selectedProject.status = this.selectedStatus;
            this.showStatusModal = false;
            await this.fetchProjects();
            this.showAlertMessage("success", result.message);
          } catch (error) {
            this.showAlertMessage("error", 'Error updating status:');
            alert('Failed to update status.');
          }
        },

        async updateProject() {
          const userType = localStorage.getItem('user_type');

              if (userType === 'staff') {
                this.showAlertMessage('error', 'You are not authorized to update a project.');
                return;
              }

            try {
              const token = sessionStorage.getItem('access_token');
              if (!token) {
                console.error('No token found');
                this.$router.push('/');
                return;
              }

              // Validate fields
              if (!this.selectedProject.project_name || !this.selectedProject.description || !this.selectedProject.project_id) {
                this.showAlertMessage('error', 'Please fill in all required fields.');
                return;
              }

              const updatedTask = {
                project_name: this.selectedProject.project_name,
                description: this.selectedProject.description,
                end_date: this.selectedProject.end_date,
                project_id: this.selectedProject.project_id
              };

              const response = await axios.put(
                `${this.baseURL}/edit_project/${this.selectedProject.project_id}`,
                updatedTask,
                {
                  headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                  },
                }
              );

              if (response.data.message) {
                this.showAlertMessage('success', response.data.message);
              }

              await this.fetchTasks();
              await this.fetchProjects();

              this.projectDetailsModal = false;
              this.selectedProject = {
                project_id: null,
                project_name: '',
                description: '',
                end_date: '',
              };

            } catch (error) {
              console.error('Error updating task:', error);
              this.showAlertMessage('error', 'Failed to update task. Please try again.');
            }
          },


    

            
  
  },
  computed: {
     Name() {
        return `${sessionStorage.getItem('firstName') || ''} ${sessionStorage.getItem('lastName') || ''}`.trim();
      },

      availableTasks() {
        return this.tasks.filter(task => task.project === null);
      },
     availableTasksForProject() {
          return this.tasks.filter(task => {
            const isUnassigned = task.project === null;
            const isAssignedToCurrent = task.project?.project_id === this.currentProjectId;
            const isSelectedForCurrent = this.selectedTasks.some(
              selected => selected.task_id === task.task_id
            );

            return isUnassigned || isAssignedToCurrent || isSelectedForCurrent;
          });
        }
  },

  mounted() {
    this.fetchTasks();
    this.fetchProjects();
    console.log("Projects array:", this.projects);
  }

};

</script>


<style scoped>
input[type="checkbox"] {
  appearance: checkbox !important;
  -webkit-appearance: checkbox !important;
  -moz-appearance: checkbox !important;
}
</style>