<template>
  <div class="min-h-screen bg-gray-100 pt-32 pb-10 px-4 sm:px-6 lg:px-8 overflow-y-auto">
    <div class="max-w-4xl mx-auto">
      <!-- Error Message -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
        {{ successMessage }}
      </div>

      <!-- Loading Indicator -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>

      <div v-else class="bg-white shadow-xl rounded-lg overflow-hidden">
        <!-- Profile Header - Made taller to accommodate the profile picture -->
        <div class="relative bg-gradient-to-r from-blue-500 to-purple-600 h-48 md:h-64">
          <!-- Profile Picture - Positioned within the header -->
          <div class="absolute left-0 bottom-0 w-full flex justify-center transform translate-y-1/2">
            <div class="relative group">
              <div class="w-36 h-36 rounded-full overflow-hidden border-4 border-white bg-gray-200 shadow-lg">
                <img 
                  :src="profileImageUrl" 
                  alt="Profile Picture" 
                  class="w-full h-full object-cover"
                  @error="handleImageError"
                />
                <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer" @click="triggerFileInput">
                  <span class="text-white text-sm font-medium">{{ uploadLoading ? 'Uploading...' : 'Change Photo' }}</span>
                </div>
              </div>
              <input 
                ref="fileInput" 
                type="file" 
                accept="image/*" 
                class="hidden" 
                @change="handleImageUpload"
              />
            </div>
        </div>
        </div>
        
        <!-- Profile Content Container - Added top padding to account for the profile picture -->
        <div class="px-4 sm:px-6 lg:px-8 pb-8 pt-20">
          <!-- Profile Information -->
          <div class="text-center mb-6">
            <h1 v-if="!editMode" class="text-3xl font-bold text-gray-800">
              {{ userProfile.firstName || '' }} {{ userProfile.lastName || '' }}
            </h1>
            <p v-if="!editMode" class="text-gray-500 text-sm mt-1">@{{ userProfile.username || 'Username not set' }}</p>
            <p v-if="!editMode" class="text-gray-500 font-semibold text-sm mt-1">{{ userProfile.user_type || 'Administrator' }}</p>
      </div>

          <!-- Edit/View Toggle -->
          <div class="text-center mb-6 space-x-4">
            <button 
              @click="toggleEditMode" 
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors cursor-pointer"
            >
              {{ editMode ? 'Cancel' : 'Edit Profile' }}
            </button>
      <button
              @click="togglePasswordMode" 
              class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors cursor-pointer"
      >
              {{ passwordMode ? 'Cancel' : 'Change Password' }}
      </button>
    </div>

          <!-- Change Password Form -->
          <div v-if="passwordMode" class="mt-8 mb-2">
            <form @submit.prevent="changePassword" class="space-y-6 max-w-md mx-auto">
      <div>
                <label for="currentPassword" class="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
        <input
                  type="password" 
                  id="currentPassword" 
                  v-model="passwordForm.currentPassword" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
        />
      </div>
      <div>
                <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-1">New Password</label>
        <input
                  type="password" 
                  id="newPassword" 
                  v-model="passwordForm.newPassword" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
        />
      </div>
      <div>
                <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">Confirm New Password</label>
                <input 
                  type="password" 
                  id="confirmPassword" 
                  v-model="passwordForm.confirmPassword" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div class="flex justify-end space-x-3">
                <button 
                  type="button" 
                  @click="passwordMode = false" 
                  class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 cursor-pointer"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 cursor-pointer"
                  :disabled="changingPassword"
                >
                  {{ changingPassword ? 'Changing Password...' : 'Change Password' }}
                </button>
              </div>
            </form>
          </div>

          <!-- View Mode -->
          <div v-if="!editMode" class="w-full backdrop-blur-lg">
            <div class="border rounded-lg p-4">
              <h2 class="text-lg font-semibold mb-4 text-gray-700">Contact Information</h2>
              <div class="space-y-3">
                <div class="flex items-start">
                  <span class="text-gray-500 w-24">Email:</span>
                  <span class="text-gray-800 flex-1">{{ userProfile.email || 'Not provided' }}</span>
                </div>
                <div class="flex items-start">
                  <span class="text-gray-500 w-24">Phone:</span>
                  <span class="text-gray-800 flex-1">{{ userProfile.contact || 'Not provided' }}</span>
                </div>
                <div class="flex items-start">
                  <span class="text-gray-500 w-24">Address:</span>
                  <span class="text-gray-800 flex-1">{{ userProfile.address || 'Not provided' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Edit Mode -->
          <div v-else class="mt-8">
            <form @submit.prevent="saveProfile" class="space-y-6">
              <!-- Personal Information -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="firstName" class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
        <input
          type="text"
                    id="firstName" 
                    v-model="editedProfile.firstName" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
                  <label for="lastName" class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
        <input
          type="text"
                    id="lastName" 
                    v-model="editedProfile.lastName" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
              </div>

              <!-- Username -->
      <div>
                <label for="username" class="block text-sm font-medium text-gray-700 mb-1">Username</label>
        <input
                  type="text" 
          id="username"
                  v-model="editedProfile.username" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

              <!-- Contact Information -->
      <div>
                <label for="contactnumber" class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
        <input
                  type="text" 
                  id="contact" 
                  v-model="editedProfile.contact" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

              <div>
                <label for="address" class="block text-sm font-medium text-gray-700 mb-1">Address</label>
                <textarea 
                  id="address" 
                  v-model="editedProfile.address" 
                  rows="3" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>

              <!-- Submit Buttons -->
              <div class="flex justify-end space-x-3">
        <button
                  type="button" 
                  @click="editMode = false" 
                  class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 cursor-pointer"
        > 
          Cancel
        </button>
        <button
                  type="submit" 
                  class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 cursor-pointer"
                  :disabled="saving"
        >
                  {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
            </form>
    </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';

export default {
  name: 'UpdateProfile',
  data() {
    return {
      userProfile: {},
      editedProfile: {},
      loading: true,
      uploadLoading: false,
      error: null,
      successMessage: null,
      editMode: false,
      passwordMode: false,
      saving: false,
      changingPassword: false,
      previewImage: null,
      allowedFileTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxFileSize: 5 * 1024 * 1024,
      apiBaseUrl: 'http://127.0.0.1:5000',
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    };
  },
  computed: {
    profileImageUrl() {
        if (this.previewImage) {
            return this.previewImage;
        }

        const img = this.userProfile?.image;
        if (img && img.trim() !== '') {
            return img.startsWith('http')
            ? img
            : `http://localhost:5000/static/uploads/${img}`;
        }

        return '/img/default_profile.png';
        }
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      this.loading = true;
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`${this.apiBaseUrl}/users/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.data.status === 'success') {
          this.userProfile = response.data.data;
          this.editedProfile = JSON.parse(JSON.stringify(this.userProfile));
          this.error = null;
          console.log('Fetched user profile:', this.userProfile);
    
        } else {
          this.error = response.data.message || 'Failed to load profile';
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
        this.error = error.response?.data?.message || 'An error occurred while loading profile';
      } finally {
        this.loading = false;
      }
    },
    
    handleImageError(event) {
      event.target.src = '/default_profile.png';
    },
    
    triggerFileInput() {
      if (!this.uploadLoading) {
        this.$refs.fileInput.click();
      }
    },
    
    previewSelectedImage(file) {
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewImage = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    
    validateFile(file) {
      if (!file) return { valid: false, message: 'No file selected' };
      
      if (!this.allowedFileTypes.includes(file.type)) {
        return { 
          valid: false, 
          message: 'Invalid file type. Please select a JPEG, PNG, GIF, or WEBP image.' 
        };
      }
      
      if (file.size > this.maxFileSize) {
        return { 
          valid: false, 
          message: `File size is too large. Maximum allowed size is ${this.maxFileSize / (1024 * 1024)}MB.` 
        };
      }
      
      return { valid: true };
    },
    
    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const validation = this.validateFile(file);
      if (!validation.valid) {
        this.error = validation.message;
        return;
      }
      
      this.previewSelectedImage(file);
      
      this.uploadLoading = true;
      this.error = null;
      
      try {
        const formData = new FormData();
        formData.append('profile_image', file);
        
        const token = localStorage.getItem('access_token');
        const response = await axios.post(`${this.apiBaseUrl}/update-profile-picture`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        });
        
        if (response.data.status === 'success') {
          this.userProfile.image = response.data.data.image_url;
          this.successMessage = 'Profile picture updated successfully';

          
          setTimeout(() => {
            this.previewImage = null;
          }, 500);
          
          setTimeout(() => {
            this.successMessage = null;
          }, 3000);
        } else {
          this.error = response.data.message || 'Failed to update profile picture';
          this.previewImage = null;
        }
      } catch (error) {
        console.error('Error uploading image:', error);
        this.error = error.response?.data?.message || 'An error occurred while uploading the image';
        this.previewImage = null;
      } finally {
        this.uploadLoading = false;
        this.$refs.fileInput.value = '';
      }
    },
    
    toggleEditMode() {
      if (this.editMode) {
        this.editedProfile = JSON.parse(JSON.stringify(this.userProfile));
      }
      this.editMode = !this.editMode;
    },
    
    togglePasswordMode() {
      this.passwordMode = !this.passwordMode;
      if (!this.passwordMode) {
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        };
      }
    },
    
    async saveProfile() {
      this.saving = true;
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.put(`${this.apiBaseUrl}/api/admin/update-profile`, {
          firstName: this.editedProfile.firstName,
          lastName: this.editedProfile.lastName,
          username: this.editedProfile.username,
          contact: this.editedProfile.contact,
          address: this.editedProfile.address
        }, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.data.status === 'success') {
          this.userProfile = { ...this.userProfile, ...this.editedProfile };
          this.editMode = false;
          this.successMessage = 'Profile updated successfully';
          
          
          document.dispatchEvent(new CustomEvent('user-profile-updated'));
          
          setTimeout(() => {
            this.successMessage = null;
          }, 3000);
        } else {
          this.error = response.data.message || 'Failed to update profile';
        }
      } catch (error) {
        console.error('Error updating profile:', error);
        this.error = error.response?.data?.message || 'An error occurred while updating profile';
      } finally {
        this.saving = false;
      }
    },

    async changePassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.error = 'New passwords do not match';
        return;
      }

      this.changingPassword = true;
      this.error = null;
      this.successMessage = null;

      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.post(
          `${this.apiBaseUrl}/api/admin/change-password`,
          {
            current_password: this.passwordForm.currentPassword,
            new_password: this.passwordForm.newPassword
          },
          {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          }
        );

        if (response.data.status === 'success') {
          this.successMessage = 'Password changed successfully';
          this.passwordMode = false;
          this.passwordForm = {
            currentPassword: '',
            newPassword: '',
            confirmPassword: ''
          };
        } else {
          this.error = response.data.message || 'Failed to change password';
        }
      } catch (error) {
        console.error('Error changing password:', error);
        this.error = error.response?.data?.message || 'An error occurred while changing password';
      } finally {
        this.changingPassword = false;
      }
    }
  }
};
</script>
  
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap');

.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}
  </style>