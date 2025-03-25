import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from './AuthContext';

const GroupsContext = createContext();

export function useGroups() {
  return useContext(GroupsContext);
}

export function GroupsProvider({ children }) {
  const { currentUser } = useAuth();
  const [groups, setGroups] = useState([]);
  const [activeGroup, setActiveGroup] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [groupMembers, setGroupMembers] = useState({});

  // Load user groups
  const loadGroups = async (silent = false) => {
    if (!currentUser) return;
    
    try {
      if (!silent) setLoading(true);
      
      const response = await api.get('/groups');
      
      if (response.data && Array.isArray(response.data)) {
        setGroups(response.data);
      } else {
        console.warn('Received invalid groups data format:', response.data);
        setGroups([]);
      }
      
      setError(null);
    } catch (err) {
      console.error('Error loading groups:', err);
      setError('Failed to load groups');
      // Keep any groups we have
      if (!groups.length) {
        setGroups([]);
      }
    } finally {
      setLoading(false);
    }
  };
  
  // Load group members
  const loadGroupMembers = async (groupId, silent = false) => {
    if (!groupId) return;
    
    try {
      if (!silent) setLoading(true);
      
      const response = await api.get(`/group/${groupId}/members`);
      
      if (response.data && Array.isArray(response.data)) {
        setGroupMembers(prev => ({
          ...prev,
          [groupId]: response.data
        }));
      } else {
        console.warn('Received invalid group members data format:', response.data);
        setGroupMembers(prev => ({
          ...prev,
          [groupId]: []
        }));
      }
    } catch (err) {
      console.error(`Error loading members for group ${groupId}:`, err);
      // Keep any members we have
      if (!groupMembers[groupId]) {
        setGroupMembers(prev => ({
          ...prev,
          [groupId]: []
        }));
      }
    } finally {
      setLoading(false);
    }
  };
  
  // Create a new group
  const createGroup = async (name) => {
    if (!name || !name.trim()) {
      throw new Error('Group name is required');
    }
    
    try {
      setLoading(true);
      
      const response = await api.post('/group', { name: name.trim() });
      
      if (response.data && response.data.id) {
        // Add the new group to state
        setGroups(prev => [...prev, response.data]);
        
        // Set as active group
        setActiveGroup(response.data.id);
        
        return response.data;
      }
      
      throw new Error('Failed to create group');
    } catch (err) {
      console.error('Error creating group:', err);
      setError('Failed to create group');
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  // Add a member to a group
  const addGroupMember = async (groupId, userId) => {
    if (!groupId || !userId) {
      throw new Error('Group ID and User ID are required');
    }
    
    try {
      setLoading(true);
      
      const response = await api.post(`/group/${groupId}/add`, { user_id: userId });
      
      if (response.data) {
        // Update group members if we have them loaded
        if (groupMembers[groupId]) {
          // Update from the response which contains updated members
          setGroupMembers(prev => ({
            ...prev,
            [groupId]: response.data.members
          }));
        }
        
        return response.data;
      }
      
      throw new Error('Failed to add member to group');
    } catch (err) {
      console.error('Error adding member to group:', err);
      setError('Failed to add member to group');
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  // Delete a group
  const deleteGroup = async (groupId) => {
    if (!groupId) {
      throw new Error('Group ID is required');
    }
    
    try {
      setLoading(true);
      
      await api.delete(`/group/${groupId}`);
      
      // Remove from state
      setGroups(prev => prev.filter(group => group.id !== groupId));
      
      // Clear active group if it was deleted
      if (activeGroup === groupId) {
        setActiveGroup(null);
      }
      
      // Clean up group members
      setGroupMembers(prev => {
        const updated = { ...prev };
        delete updated[groupId];
        return updated;
      });
      
      return true;
    } catch (err) {
      console.error('Error deleting group:', err);
      setError('Failed to delete group');
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  // Leave a group
  const leaveGroup = async (groupId) => {
    if (!groupId) {
      throw new Error('Group ID is required');
    }
    
    try {
      setLoading(true);
      
      await api.delete(`/group/${groupId}/leave`);
      
      // Remove from state
      setGroups(prev => prev.filter(group => group.id !== groupId));
      
      // Clear active group if it was the group we left
      if (activeGroup === groupId) {
        setActiveGroup(null);
      }
      
      // Clean up group members
      setGroupMembers(prev => {
        const updated = { ...prev };
        delete updated[groupId];
        return updated;
      });
      
      return true;
    } catch (err) {
      console.error('Error leaving group:', err);
      setError('Failed to leave group');
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  // Get group details
  const getGroupDetails = async (groupId) => {
    if (!groupId) {
      throw new Error('Group ID is required');
    }
    
    try {
      setLoading(true);
      
      const response = await api.get(`/group/${groupId}`);
      
      if (response.data) {
        // Update members for this group
        setGroupMembers(prev => ({
          ...prev,
          [groupId]: response.data.members
        }));
        
        // Update group in groups array
        setGroups(prev => 
          prev.map(group => 
            group.id === groupId ? { ...group, ...response.data } : group
          )
        );
        
        return response.data;
      }
      
      throw new Error('Failed to get group details');
    } catch (err) {
      console.error('Error getting group details:', err);
      setError('Failed to get group details');
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  // Refresh groups
  const refreshGroups = async (silent = false) => {
    await loadGroups(silent);
    return true;
  };
  
  // Load groups when user logs in
  useEffect(() => {
    if (currentUser) {
      loadGroups();
    } else {
      // Clear groups when user logs out
      setGroups([]);
      setActiveGroup(null);
      setGroupMembers({});
    }
  }, [currentUser]);
  
  // When active group changes, load members if not already loaded
  useEffect(() => {
    if (activeGroup && !groupMembers[activeGroup]) {
      loadGroupMembers(activeGroup);
    }
  }, [activeGroup]);

  const value = {
    groups,
    activeGroup,
    setActiveGroup,
    loading,
    error,
    groupMembers,
    loadGroups,
    refreshGroups,
    loadGroupMembers,
    createGroup,
    addGroupMember,
    deleteGroup,
    leaveGroup,
    getGroupDetails
  };

  return (
    <GroupsContext.Provider value={value}>
      {children}
    </GroupsContext.Provider>
  );
} 