'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Sparkles, MessageCircle, ArrowRight } from 'lucide-react';
import { HERO_CONTENT, ANIMATION_DELAYS } from '@/constants';

export default function Hero() {
    return (
        <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 overflow-hidden">

            <div className="absolute inset-0 bg-gradient-to-br from-makers-green/5 to-makers-purple/5" />

            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="space-y-8"
                >

                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: ANIMATION_DELAYS.HERO_BADGE, duration: 0.5 }}
                        className="inline-flex items-center space-x-2 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-full px-4 py-2 text-sm text-gray-600"
                    >
                        <Sparkles className="w-4 h-4 text-orange-500" />
                        <span>{HERO_CONTENT.BADGE_TEXT}</span>
                    </motion.div>

                    <motion.h1
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: ANIMATION_DELAYS.HERO_TITLE, duration: 0.6 }}
                        className="text-5xl md:text-7xl font-bold text-makers-purple leading-tight"
                    >
                        {HERO_CONTENT.TITLE}
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: ANIMATION_DELAYS.HERO_DESCRIPTION, duration: 0.6 }}
                        className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed"
                    >
                        {HERO_CONTENT.DESCRIPTION}
                    </motion.p>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: ANIMATION_DELAYS.HERO_CTA, duration: 0.6 }}
                    >
                        <Link
                            href="/chat"
                            className="inline-flex items-center space-x-3 bg-teal-600 text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-teal-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
                        >
                            <MessageCircle className="w-5 h-5" />
                            <span>{HERO_CONTENT.CTA_TEXT}</span>
                            <ArrowRight className="w-5 h-5" />
                        </Link>
                    </motion.div>
                </motion.div>
            </div>

            <div className="absolute top-20 left-10 w-20 h-20 bg-makers-green/20 rounded-full blur-xl" />
            <div className="absolute bottom-20 right-10 w-32 h-32 bg-makers-purple/20 rounded-full blur-xl" />
        </section>
    );
} 