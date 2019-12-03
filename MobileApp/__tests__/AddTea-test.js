/**
 * @format
 */

import 'react-native';
import React from 'react';
import { AddTea } from '../AddTea.js';
import { shallow } from 'enzyme';
import * as socketUtil from '../socketUtil';

const mockInput = [
    {
      name: 'Good Tea', 
      steepTime: '120', 
      temp:'70',
      expected: true 
    },
    { 
      name: '', 
      steepTime: '120', 
      temp:'70',
      expected: false 
    },
    { 
      name: 'Bad!Tea!Name', 
      steepTime: '120', 
      temp:'70',
      expected: false 
    },
    {
      name: 'Tea', 
      steepTime: 'invalid', 
      temp:'70',
      expected: false 
    },
    { 
      name: 'Tea', 
      steepTime: '2000', 
      temp:'70',
      expected: false 
    },
    {
      name: 'Tea', 
      steepTime: '120', 
      temp:'invalid',
      expected: false 
    },
    { 
      name: 'Tea', 
      steepTime: '2000', 
      temp:'50',
      expected: false 
    }
]

describe('Validate user input where', () => {
  const wrapper = shallow(<AddTea />)
  const instance = wrapper.instance();
  global.alert = jest.fn();
  let index = -1;
  let inputValidationResult
  beforeEach(() => {
    index++;
    inputValidationResult = instance.validateInputs(mockInput[index].name, mockInput[index].steepTime, mockInput[index].temp)
  })
  it('user inputs are all correct', () => {
    expect(inputValidationResult).toBe(mockInput[index].expected)
  })
  it('Empty tea profile name', () => {
    expect(inputValidationResult).toBe(mockInput[index].expected)
  })
  it('Bad tea profile name', () => {
    expect(inputValidationResult).toBe(mockInput[index].expected)
  })
  it('Non-numeric character in steep time', () => {
    expect(inputValidationResult).toBe(mockInput[index].expected)
  })
  it('Out of bound steep time', () => {
    expect(inputValidationResult).toBe(mockInput[index].expected)
  })
  it('Non-numeric character in temperature', () => {
    expect(inputValidationResult).toBe(mockInput[index].expected)
  })
  it('Out of bound temperature', () => {
    expect(inputValidationResult).toBe(mockInput[index].expected)
  })
})

describe('Submitting new tea profile', () => {
  const wrapper = shallow(<AddTea />)
  const instance = wrapper.instance();
  let newTeaProfileArray = [];
  wrapper.setProps({ 
    navigation: { 
      state: { params: { teas: [] }}, 
      // navigate: jest.fn((screen, data) => newTeaProfileArray = data.teas)
    }
  })
  beforeEach(() => {
    newTeaProfileArray = [];
    socketUtil.send = jest.fn()
    socketUtil.listen = jest.fn()
  })
  it('input validation - success', () => {
    instance.validateInputs = jest.fn(() => true)
    instance.onSubmit()
    expect(socketUtil.send).toBeCalled()
    expect(socketUtil.listen).toBeCalled()
  }) 
  it('input validation - fail', () => {
    instance.validateInputs = jest.fn(() => false)
    instance.onSubmit()
    expect(socketUtil.send).not.toBeCalled()
    expect(socketUtil.listen).not.toBeCalled()
  }) 
})