import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronUp } from "lucide-react";

const faqs = [
  {
    question: "What is GEON?",
    answer:
      "GEON is an AI-powered growth platform tailored for modern digital brands. It helps you increase visibility across AI-driven search engines, optimize content for better rankings, and gain actionable insights through intelligent data analysis. GEON acts as your digital growth assistant, ensuring that your brand reaches the right audience efficiently and effectively.",
  },
  {
    question: "How does GEON help in brand growth?",
    answer:
      "GEON leverages advanced algorithms and real-time optimization to enhance your brand's discoverability. By analyzing how generative AI models and modern search engines evaluate and rank content, GEON fine-tunes your website and digital presence to align with these evolving systems. This ensures your brand is surfaced more often, in more relevant contexts, and to the most targeted audiences — ultimately driving traffic, engagement, and conversions.",
  },
  {
    question: "Is GEON suitable for early-stage startups?",
    answer:
      "Absolutely. GEON is designed with flexibility in mind, making it ideal for early-stage startups that are building their online presence. It provides easy-to-use tools, smart recommendations, and scalable analytics that grow with your company. Whether you have a small website or are preparing for rapid scaling, GEON adapts to your needs and helps you lay a strong foundation for future growth.",
  },
  {
    question: "What features does GEON offer?",
    answer:
      "GEON offers a powerful suite of features including AI-powered search engine optimization tailored for generative engines, detailed performance analytics, growth opportunity detection, keyword monitoring, competitor benchmarking, and customizable dashboards for tracking KPIs. All features are built to work seamlessly and deliver real-time, actionable insights that empower your growth and content teams.",
  },
  {
    question: "Do I need technical knowledge to use GEON?",
    answer:
      "Not at all. GEON is built for simplicity and usability. Its intuitive user interface requires no coding skills, allowing marketers, founders, and growth teams to navigate, analyze, and act on insights without relying on engineers. The platform does all the heavy lifting in the background, so you can focus on making data-driven decisions that matter.",
  },
  {
    question: "Can I try GEON before committing?",
    answer:
      "Yes! GEON offers a no-risk free trial so you can explore the full capabilities of the platform before making any decisions. During the trial, you'll have access to core features, personalized recommendations, and performance insights. This way, you can evaluate how GEON fits into your workflow and supports your growth objectives before committing to a paid plan.",
  },
];


export default function FAQ() {
  const [openIndex, setOpenIndex] = useState(null);

  const toggle = (index) => {
    setOpenIndex(index === openIndex ? null : index);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="bg-[hsl(220,20%,8%)] text-white py-12 px-4 md:px-24"
    >
      <motion.h2
        initial={{ y: -30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="text-4xl font-bold text-center mb-10"
      >
        Frequently Asked Questions
      </motion.h2>

      {/* Centered FAQ container */}
      <div className="flex justify-center">
        <div className="space-y-4 w-full max-w-4xl">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              viewport={{ once: true }}
              className="border border-gray-700 rounded-lg bg-[hsl(220,20%,10%)]"
            >
              <button
                onClick={() => toggle(index)}
                className="w-full flex items-center justify-between px-6 py-4 text-left text-lg font-thin focus:outline-none"
              >
                {faq.question}
                {openIndex === index ? <ChevronUp /> : <ChevronDown />}
              </button>

              <AnimatePresence>
                {openIndex === index && (
                  <motion.div
                    key="content"
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0 }}
                    className="px-6 pb-4 text-gray-300 overflow-hidden"
                  >
                    {faq.answer}
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
