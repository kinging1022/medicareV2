
<template>
  <main class="flex-1">
    <!-- Landing Section -->
    <section class="w-full py-12 md:py-24 lg:py-32 xl:py-48 bg-gradient-to-br from-blue-50 via-green-50 to-teal-50">
      <div class="container mx-auto px-4 md:px-6 lg:px-8">
        <div class="flex flex-col items-center space-y-4 text-center">
          <h1 class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none text-gray-900">
            Your Health, Our Priority
          </h1>
          <p class="mx-auto max-w-[700px] text-gray-600 md:text-xl dark:text-gray-400">
            Medicare: Empowering you with comprehensive healthcare solutions.
          </p>
          <div class="space-x-4">
            <Button class="bg-teal-500 text-white hover:bg-teal-600">Get Started</Button>
            <Button variant="outline" class="text-teal-500 border-teal-500 hover:bg-teal-50">Learn More</Button>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="w-full py-12 md:py-24 lg:py-32 bg-white">
      <div class="container mx-auto px-4 md:px-6 lg:px-8">
        <h2 class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-center mb-12 text-gray-900">
          Why Choose Medicare?
        </h2>
        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <FeatureCard
            v-for="(feature, index) in features"
            :key="index"
            :icon="feature.icon"
            :title="feature.title"
            :description="feature.description"
          />
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import FeatureCard from '@/components/FeatureCard.vue';
import Button from '@/components/ui/button.vue';



export default {
components: {
  FeatureCard,
  Button,


},
data() {
  return {
    isMenuOpen: false,
    features: [
      { icon: "Users", title: "Patient-Centric Care", description: "Tailored healthcare experiences designed around your needs." },
      { icon: "CalendarRange", title: "24/7 Availability", description: "Access medical support anytime, day or night." },
      { icon: "Stethoscope", title: "Expert Physicians", description: "Connect with top-rated doctors across various specialties." },
      { icon: "Shield", title: "Secure & Confidential", description: "Your health data is protected with state-of-the-art security." },
      { icon: "Award", title: "Quality Assurance", description: "Rigorous standards ensure you receive the best care possible." },
      { icon: "Heart", title: "Holistic Approach", description: "Comprehensive care addressing both physical and mental health." },
    ]
  };
},
methods: {

}
};
</script>



