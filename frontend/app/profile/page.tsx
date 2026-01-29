'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { useStore } from '@/lib/store';
import { useAuth } from '@/contexts/AuthContext';

export default function ProfilePage() {
  const { user } = useStore();
  const { signOut } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    bio: 'Passionate learner exploring AI and modern development techniques.'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // In a real app, we would save this to the backend
    console.log('Profile updated:', formData);
    setIsEditing(false);
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-sky-100 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Please sign in</h2>
          <p className="text-gray-600 mb-6">You need to be signed in to view your profile.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-sky-100">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-gradient-to-br from-white via-sky-50 to-purple-50 rounded-lg shadow-lg overflow-hidden border border-sky-200">
          <div className="p-6">
            <div className="flex justify-between items-start mb-6">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-sky-600 to-purple-600 bg-clip-text text-transparent">Your Profile</h1>

              <Button
                variant="outline"
                onClick={() => signOut()}
                className="border-sky-400 text-sky-600 hover:bg-sky-50"
              >
                Sign out
              </Button>
            </div>

            <div className="flex flex-col md:flex-row gap-8">
              <div className="md:w-1/3">
                <div className="bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100 border-2 border-sky-300 rounded-full w-32 h-32 mx-auto flex items-center justify-center shadow-lg">
                  <div className="text-4xl font-bold text-sky-600">
                    {user.name.charAt(0).toUpperCase()}
                  </div>
                </div>

                <div className="mt-4 text-center bg-gradient-to-br from-sky-50 to-purple-50 p-4 rounded-lg border border-sky-200">
                  <p className="text-lg font-bold bg-gradient-to-r from-sky-600 to-purple-600 bg-clip-text text-transparent">{user.name}</p>
                  <p className="text-gray-600 text-sm mt-1">{user.email}</p>

                  <div className="mt-4">
                    <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold shadow-md ${
                      user.tier === 'premium'
                        ? 'bg-gradient-to-r from-purple-400 to-pink-400 text-white'
                        : 'bg-gradient-to-r from-green-400 to-sky-400 text-white'
                    }`}>
                      ✨ {user.tier.charAt(0).toUpperCase() + user.tier.slice(1)}
                    </span>
                  </div>
                </div>
              </div>

              <div className="md:w-2/3">
                {isEditing ? (
                  <form onSubmit={handleSubmit}>
                    <div className="mb-6">
                      <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                        Full Name
                      </label>
                      <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        required
                      />
                    </div>

                    <div className="mb-6">
                      <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                        Email Address
                      </label>
                      <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        required
                      />
                    </div>

                    <div className="mb-6">
                      <label htmlFor="bio" className="block text-sm font-medium text-gray-700 mb-1">
                        Bio
                      </label>
                      <textarea
                        id="bio"
                        name="bio"
                        value={formData.bio}
                        onChange={handleChange}
                        rows={4}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      ></textarea>
                    </div>

                    <div className="flex space-x-3">
                      <Button type="submit">
                        Save Changes
                      </Button>
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => setIsEditing(false)}
                      >
                        Cancel
                      </Button>
                    </div>
                  </form>
                ) : (
                  <div>
                    <div className="mb-6 bg-gradient-to-br from-blue-50 to-purple-50 p-6 rounded-lg border border-blue-200 shadow-sm">
                      <h2 className="text-lg font-semibold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">Personal Information</h2>

                      <div className="space-y-4">
                        <div className="bg-white/50 p-3 rounded-md">
                          <p className="text-sm text-sky-600 font-medium">Full Name</p>
                          <p className="text-gray-900 font-semibold">{formData.name}</p>
                        </div>

                        <div className="bg-white/50 p-3 rounded-md">
                          <p className="text-sm text-sky-600 font-medium">Email Address</p>
                          <p className="text-gray-900 font-semibold">{formData.email}</p>
                        </div>

                        <div className="bg-white/50 p-3 rounded-md">
                          <p className="text-sm text-sky-600 font-medium">Bio</p>
                          <p className="text-gray-900">{formData.bio}</p>
                        </div>
                      </div>
                    </div>

                    <div className="mb-6 bg-gradient-to-br from-green-50 to-sky-50 p-6 rounded-lg border border-green-200 shadow-sm">
                      <h2 className="text-lg font-semibold bg-gradient-to-r from-green-600 to-sky-600 bg-clip-text text-transparent mb-4">Account Information</h2>

                      <div className="space-y-4">
                        <div className="bg-white/50 p-3 rounded-md">
                          <p className="text-sm text-green-600 font-medium">Member Since</p>
                          <p className="text-gray-900 font-semibold">January 15, 2023</p>
                        </div>

                        <div className="bg-white/50 p-3 rounded-md">
                          <p className="text-sm text-green-600 font-medium">Account Tier</p>
                          <p className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold shadow-sm ${
                            user.tier === 'premium'
                              ? 'bg-gradient-to-r from-purple-400 to-pink-400 text-white'
                              : 'bg-gradient-to-r from-green-400 to-sky-400 text-white'
                          }`}>
                            ✨ {user.tier.charAt(0).toUpperCase() + user.tier.slice(1)} Account
                          </p>
                        </div>
                      </div>
                    </div>

                    <Button
                      onClick={() => setIsEditing(true)}
                      className="bg-gradient-to-r from-sky-500 to-purple-500 hover:from-sky-600 hover:to-purple-600 text-white shadow-md"
                    >
                      ✏️ Edit Profile
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}