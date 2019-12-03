<template>
  <div class="row">
    <div class="col-md-8">
      <edit-profile-form :model="model">
      </edit-profile-form>
    </div>
    <div class="col-md-4">
      <user-card :user="user"></user-card>
    </div>
  </div>
</template>
<script>
  import EditProfileForm from './Profile/EditProfileForm';
  import UserCard from './Profile/UserCard'
  import axios from "axios";

  var username_ = "Default";
  var device_ = "1231";

  export default {
    components: {
      EditProfileForm,
      UserCard
    },
    data() {
      return {
        model: {
          device: device_,
          username: username_,
        },
        user: {
          fullName: 'Mike Andrew',
          title: 'Ceo/Co-Founder',
          description: `Do not be scared of the truth because we need to restart the human foundation in truth And I love you like Kanye loves Kanye I love Rick Owens’ bed design but the back is...`,
        }
      }
    },
    mounted() {
  }
  }
</script>
<style>
</style>
