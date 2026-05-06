// Initialize Lenis for smooth scrolling
const lenis = new Lenis({
  duration: 0.8, // Reduced from 1.2
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  orientation: "vertical",
  gestureOrientation: "vertical",
  smoothWheel: true
});

// Register ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger, CustomEase);

// Sync Lenis with ScrollTrigger
lenis.on("scroll", ScrollTrigger.update);

gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});

gsap.ticker.lagSmoothing(0);

// Custom eases
CustomEase.create("softReveal", "0.5, 0, 0, 1");
CustomEase.create("smoothBlur", "0.25, 0.1, 0.25, 1");

// Video animation
const videoContainer = document.getElementById("video-container");
const video = document.getElementById("video");
const videoOverlay = document.querySelector(".video-overlay");
const overlayCaption = document.querySelector(".video-overlay .caption");
const overlayContent = document.querySelector(".video-overlay .content");
const overlayTitle = document.querySelector(".video-overlay h2");
const overlayTexts = document.querySelectorAll(".video-overlay p");
const mountainFooter = document.querySelector(".mountain-footer");
const footerVideo = document.querySelector(".mountain-footer video");

// Email functionality removed - now a direct contact link

// Ensure video plays
video.play().catch((error) => {
  console.log("Video play failed: ", error);
});

// Create timeline for video animation
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".scroll-container",
    start: "top top",
    end: "bottom bottom",
    scrub: 1.2, // Increased for smoother motion
    markers: false,
    onEnter: () => video.play()
  }
});

// Hero section animation removed - replaced by static banner

// Create a background overlay for darkening effect
const overlay = document.createElement("div");
overlay.style.position = "absolute";
overlay.style.top = "0";
overlay.style.left = "0";
overlay.style.width = "100%";
overlay.style.height = "100%";
overlay.style.backgroundColor = "rgba(0,0,0,0)";
overlay.style.pointerEvents = "none";
overlay.style.zIndex = "1"; // Lower than text overlay
videoContainer.appendChild(overlay);

// Animate video container with darkening overlay
tl.to(
  videoContainer,
  {
    width: "90vw",
    height: "90vh",
    borderRadius: "0",
    ease: "expo.out", // More dynamic easing
    duration: 0.5
  },
  0
)
  .to(
    video,
    {
      scale: 1.1, // Zoom in the video slightly
      ease: "expo.out",
      duration: 0.5
    },
    0
  )
  .to(
    overlay,
    {
      backgroundColor: "rgba(0,0,0,0.4)", // Darken overlay while scrolling
      ease: "power3.inOut", // Improved easing
      duration: 0.5
    },
    0
  )
  .to(
    videoOverlay,
    {
      clipPath: "inset(0% 0 0 0)",
      backdropFilter: "blur(8px)",
      ease: "expo.out", // More dynamic easing
      duration: 0.3
    },
    0.4
  ) // Delay until container is 80% of full size
  .to(
    overlayCaption,
    {
      transform: "translateY(0)",
      ease: "expo.out",
      duration: 0.3
    },
    0.45
  ) // Slightly earlier than before
  .to(
    overlayContent,
    {
      filter: "blur(0px)", // Unblur the content
      transform: "scale(1)", // Reset scale to normal
      ease: "expo.out",
      duration: 0.4
    },
    0.45
  );

// Footer animation
gsap.to(mountainFooter, {
  scrollTrigger: {
    trigger: ".footer-content",
    start: "top 80%",
    end: "top 40%",
    scrub: 1.2, // Slower scrub for smoother motion
    onEnter: () => footerVideo.play(),
    markers: false
  },
  clipPath: "inset(0% 0 0 0)",
  ease: "expo.out", // More dynamic easing
  duration: 1
});

// Contact button animation in footer
gsap.to(".mountain-footer .contact-btn", {
  scrollTrigger: {
    trigger: ".mountain-footer",
    start: "top 60%",
    end: "top 40%",
    scrub: 0.8,
    markers: false
  },
  opacity: 1,
  ease: "expo.out",
  duration: 0.5
});

// Text reveal animations
gsap.utils.toArray(".footer-content p").forEach((text) => {
  gsap.from(text, {
    scrollTrigger: {
      trigger: text,
      start: "top 85%",
      end: "top 70%",
      scrub: 1.2 // Slower scrub for smoother motion
    },
    y: 15,
    filter: "blur(5px)",
    ease: "expo.out" // More dynamic easing
  });
});

// Refresh ScrollTrigger to ensure correct positions after layout changes
ScrollTrigger.refresh();