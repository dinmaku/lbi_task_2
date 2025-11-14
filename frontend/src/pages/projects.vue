<template>
   <div class="min-h-screen bg-gray-100 py-10 px-12 overflow-y-auto">
    <div class="flex flex-row justify-between items-start">
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
                <button class="mt-5 px-2 py-3 bg-blue-500 text-gray-100 rounded-lg font-semibold">Today's Schedule</button>
             </div>
              <img src="../assets/icons/office.png" class="mr-20 w-1/5 h-auto" alt="">
          </div>
       </div>
 
       <div class="flex flex-row justify-start">
       <div class="grid grid-cols-3 mt-10 space-y-5 gap-x-6">
          <div
           v-for="project in projects"
           :key="project.id"
           class="w-[390px] h-auto bg-blue-50 border border-gray-300 rounded-xl shadow-md p-5 transition-transform duration-300 transform hover:scale-105 cursor-pointer space-y-5">
              <h2 class="text-lg font-semibold text-gray-400 text-start"> {{ project.dateCreated }}</h2>
              <div class="flex justify-between items-center">
                <div class="flex flex-col text-left">
                <h2 class="text-2xl text-gray-700 font-semibold">{{ project.name }}</h2>
                <p class="text-md text-blue-400 ">Contains <span class="text-blue-600 font-semibold">{{ project.tasks }}</span> tasks</p>
                </div>
                <span class="px-2 py-1 text-xs rounded-full"
                      :class="statusClass(project.status)"
                >{{ project.status }}</span>
              </div>

          <div>
            <div class="w-full bg-gray-200 rounded-full h-3 ">
                <div class="h-3 rounded-full"
                    :class="progressColor(project.status)"
                    :style="{ width: project.progress + '%'}">
                </div>
                <div class="flex justify-between items-center font-semibold mt-1 text-gray-400">
                  <p>Progress</p>
                  <p class="text-gray-700">{{ project.progress }}%</p>
                </div>
                
            </div>
          </div>
              <hr class="my-12 border-gray-300" />
           <div class="flex justify-between items-center mt-9">
                   <div class="flex flex-row gap-x-1">
                    <img src="../assets/icons/folder.png" class="w-6 h-6" alt="">
                <button title="Add Task" class="w-6 h-6 flex items-center justify-center rounded-full text-xl text-white font-bold cursor-pointer"
                        :class="statusBg(project.status)"><span class="mb-1">+</span></button>
                    </div>
                <div class="py-1 px-2 flex items-center justify-center rounded-full text-sm text-white font-semibold"
                     :class="statusBg(project.status)">
                <p>{{ project.deadline }} days left</p>
                </div>
           </div>

         
  
   
           
                </div>
            </div>
        </div>
      </div>
      
          <div class="w-full max-w-md mx-auto p-4 bg-white rounded-lg shadow-md">
          <!-- Header -->
          <div class="flex justify-between items-center mb-4">
            <button @click="prevMonth" class="px-2 py-1 rounded hover:bg-gray-200">&lt;</button>
            <h2 class="text-lg font-semibold">{{ monthYear }}</h2>
            <button @click="nextMonth" class="px-2 py-1 rounded hover:bg-gray-200">&gt;</button>
          </div>

          <!-- Weekdays -->
          <div class="grid grid-cols-7 gap-1 text-center font-medium text-gray-500 mb-2">
            <div v-for="day in weekdays" :key="day">{{ day }}</div>
          </div>

          <!-- Dates -->
          <div class="grid grid-cols-7 gap-1 text-center">
            <div 
              v-for="(date, index) in calendarDays" 
              :key="index"
              :class="[
                'py-2 rounded cursor-pointer',
                date.isCurrentMonth ? 'text-gray-800' : 'text-gray-300',
                date.isToday ? 'bg-black text-white' : '',
                date.isSelected ? 'bg-purple-600 text-white' : ''
              ]"
              @click="selectDate(date)"
            >
              {{ date.date.getDate() }}
            </div>
          </div>
        </div>
      </div> 
   </div>
</template>
<script>

export default {
  name: "Projects",

 data() {
    return {
      projects: [
        {
          id: 1,
          name: "Website Redesign",
          status: "Draft",
          progress: 10,
          tasks: 3,
          dateCreated: "Nov 1, 2025",
          deadline: 12,
        },
        {
          id: 2,
          name: "Mobile App",
          status: "In Progress",
          progress: 45,
          tasks: 8,
          dateCreated: "Oct 20, 2025",
          deadline: 20,
        },
        {
          id: 3,
          name: "API Integration",
          status: "For QA",
          progress: 70,
          tasks: 5,
          dateCreated: "Sept 20, 2025",
          deadline: 5,
        },
        {
          id: 4,
          name: "Deployment",
          status: "In Production",
          progress: 90,
          tasks: 10,
          dateCreated: "Oct 10, 2025",
          deadline: 2,
        },
        {
          id: 5,
          name: "Final Report",
          status: "Complete",
          progress: 100,
          tasks: 12,
          dateCreated: "July 2, 2025",
          deadline: 0,
        },
      ],
      currentDate: new Date(),
      selectedDate: null,
      weekdays: ['M','T','W','TH','F']
    };
  },

  methods: {

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
          case "Complete":
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
        case "Complete":
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

    prevMonth() {
      this.currentDate.setMonth(this.currentDate.getMonth() - 1);
      this.currentDate = new Date(this.currentDate);
    },
    nextMonth() {
      this.currentDate.setMonth(this.currentDate.getMonth() + 1);
      this.currentDate = new Date(this.currentDate);
    },
     selectDate(dateObj) {
      this.selectedDate = dateObj.date;
    },
    isToday(date) {
      const today = new Date();
      return today.getFullYear() === date.getFullYear() &&
             today.getMonth() === date.getMonth() &&
             today.getDate() === date.getDate();
    },
    isSameDate(date1, date2) {
      return date1.getFullYear() === date2.getFullYear() &&
             date1.getMonth() === date2.getMonth() &&
             date1.getDate() === date2.getDate();
    }
    
  
  },
  computed: {
     Name() {
        return `${sessionStorage.getItem('firstName') || ''} ${sessionStorage.getItem('lastName') || ''}`.trim();
      },
      monthYear() {
        return this.currentDate.toLocaleString('default', { month: 'long', year:'numeric'});
      },
      monthYear() {
      return this.currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });
    },
    calendarDays() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();

      const firstDayOfMonth = new Date(year, month, 1);
      const lastDayOfMonth = new Date(year, month + 1, 0);

      // Find the start of the calendar (Monday)
      const startDay = firstDayOfMonth.getDay() === 0 ? 6 : firstDayOfMonth.getDay() - 1;
      const totalDays = lastDayOfMonth.getDate() + startDay;

      const days = [];
      for (let i = 0; i < totalDays; i++) {
        const date = new Date(year, month, i - startDay + 1);
        days.push({
          date,
          isCurrentMonth: date.getMonth() === month,
          isToday: this.isToday(date),
          isSelected: this.selectedDate && this.isSameDate(date, this.selectedDate),
        });
      }
      return days;
    }


  },

};

</script>


<style scoped>
</style>