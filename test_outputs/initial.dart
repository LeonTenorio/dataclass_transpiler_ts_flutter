import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:package:dartz/dartz.dart';
import './hive_type_ids.dart';
import './index.dart';
import 'dart:convert';

part 'initial.freezed.dart';
part 'initial.g.dart';


/// Basic type 
@freezed
class BasicType with _$BasicType {
  static ModelsBox<BasicType, BasicType> getBox() {
    return ModelsBox<BasicType, BasicType>(
      boxKey: HiveTypeIds.BasicType.toString(),
      boxValueToValue: (value) => value,
      valueToBoxValue: (value) => value,
    );
  }

  @HiveTypeId(typeId: HiveTypeIds.BasicType)
  const factory BasicType({
    /// Basic type a object field comment 
    required String a,
    required String b,
    required String c,
  }) = _BasicType;

  factory BasicType.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$BasicTypeFromJson(json);
}

class BasicTypeWithNullableAndOptional with _$BasicTypeWithNullableAndOptional {
  const factory BasicTypeWithNullableAndOptional({
    required String ? a,
    String b,
    required String c,
  }) = _BasicTypeWithNullableAndOptional;

  factory BasicTypeWithNullableAndOptional.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$BasicTypeWithNullableAndOptionalFromJson(json);
}

class TypeWithUnionMainUnionType with _$TypeWithUnionMainUnionType {
  const factory TypeWithUnionMainUnionType({
    required String c,
    required String d,
  }) = _TypeWithUnionMainUnionType;

  factory TypeWithUnionMainUnionType.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$TypeWithUnionMainUnionTypeFromJson(json);
}
class TypeWithUnion{
  late final Object _value;

  TypeWithUnion.fromJson(Map<String, dynamic> json){
    final deserializationFunctions = [
      (json) => BasicType.fromJson(json),
      (json) => TypeWithUnionMainUnionType.fromJson(json),
    ];

    for(final deserializationFunction in deserializationFunctions){
      try{
        _value = deserializationFunction(json);
      } catch (_) {}
    }
  }

  Map<String, dynamic> toJson(){
    final List<Tuple2<bool Function(), Map<String, dynamic> Function()>> evaluateClasses = [
      Tuple2(this.isBasicType, this.asBasicType),
      Tuple2(this.isTypeWithUnionMainUnionType, this.asTypeWithUnionMainUnionType),
    ];

    for(final evaluateClass in evaluateClasses){
      final isClass = evaluateClass.value1();
      if(isClass()){
        return evaluateClass.value2().toJson();
      }
    }
  }

  TypeWithUnion.fromValue({
    BasicType? basicType,
    TypeWithUnionMainUnionType? typeWithUnionMainUnionType,
  }){
    _value = (
      basicType??
      typeWithUnionMainUnionType
    )!;
  }


  bool isBasicType() {
    return _value is BasicType;
  }

  BasicType asBasicType(){
    return _value as BasicType;
  }

  bool isTypeWithUnionMainUnionType() {
    return _value is TypeWithUnionMainUnionType;
  }

  TypeWithUnionMainUnionType asTypeWithUnionMainUnionType(){
    return _value as TypeWithUnionMainUnionType;
  }

}

@freezed
class TypeWithMultipleUnionMainUnionType with _$TypeWithMultipleUnionMainUnionType {
  static ModelsBox<TypeWithMultipleUnionMainUnionType, TypeWithMultipleUnionMainUnionType> getBox() {
    return ModelsBox<TypeWithMultipleUnionMainUnionType, TypeWithMultipleUnionMainUnionType>(
      boxKey: HiveTypeIds.TypeWithMultipleUnionMainUnionType.toString(),
      boxValueToValue: (value) => value,
      valueToBoxValue: (value) => value,
    );
  }

  const factory TypeWithMultipleUnionMainUnionType({
    required String c,
    required String d,
  }) = _TypeWithMultipleUnionMainUnionType;

  factory TypeWithMultipleUnionMainUnionType.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$TypeWithMultipleUnionMainUnionTypeFromJson(json);
}
class TypeWithMultipleUnion{
  late final Object _value;

  TypeWithMultipleUnion.fromJson(Map<String, dynamic> json){
    final deserializationFunctions = [
      (json) => BasicType.fromJson(json),
      (json) => BasicTypeWithNullableAndOptional.fromJson(json),
      (json) => TypeWithMultipleUnionMainUnionType.fromJson(json),
    ];

    for(final deserializationFunction in deserializationFunctions){
      try{
        _value = deserializationFunction(json);
      } catch (_) {}
    }
  }

  Map<String, dynamic> toJson(){
    final List<Tuple2<bool Function(), Map<String, dynamic> Function()>> evaluateClasses = [
      Tuple2(this.isBasicType, this.asBasicType),
      Tuple2(this.isBasicTypeWithNullableAndOptional, this.asBasicTypeWithNullableAndOptional),
      Tuple2(this.isTypeWithMultipleUnionMainUnionType, this.asTypeWithMultipleUnionMainUnionType),
    ];

    for(final evaluateClass in evaluateClasses){
      final isClass = evaluateClass.value1();
      if(isClass()){
        return evaluateClass.value2().toJson();
      }
    }
  }

  TypeWithMultipleUnion.fromValue({
    BasicType? basicType,
    BasicTypeWithNullableAndOptional? basicTypeWithNullableAndOptional,
    TypeWithMultipleUnionMainUnionType? typeWithMultipleUnionMainUnionType,
  }){
    _value = (
      basicType??
      basicTypeWithNullableAndOptional??
      typeWithMultipleUnionMainUnionType
    )!;
  }

  static ModelsBox<TypeWithMultipleUnion, String> getBox() {
    return ModelsBox<TypeWithMultipleUnion, String>(
      boxKey: HiveTypeIds.TypeWithMultipleUnion.toString(),
      boxValueToValue: (value) => TypeWithMultipleUnion.fromJson(json.decode(value)),
      valueToBoxValue: (value) => json.encode(TypeWithMultipleUnion.toJson()),
    );
  }


  bool isBasicType() {
    return _value is BasicType;
  }

  BasicType asBasicType(){
    return _value as BasicType;
  }

  bool isBasicTypeWithNullableAndOptional() {
    return _value is BasicTypeWithNullableAndOptional;
  }

  BasicTypeWithNullableAndOptional asBasicTypeWithNullableAndOptional(){
    return _value as BasicTypeWithNullableAndOptional;
  }

  bool isTypeWithMultipleUnionMainUnionType() {
    return _value is TypeWithMultipleUnionMainUnionType;
  }

  TypeWithMultipleUnionMainUnionType asTypeWithMultipleUnionMainUnionType(){
    return _value as TypeWithMultipleUnionMainUnionType;
  }

}

@freezed
class TypeWithIntersectionMainIntersectionType with _$TypeWithIntersectionMainIntersectionType {
  static ModelsBox<TypeWithIntersectionMainIntersectionType, TypeWithIntersectionMainIntersectionType> getBox() {
    return ModelsBox<TypeWithIntersectionMainIntersectionType, TypeWithIntersectionMainIntersectionType>(
      boxKey: HiveTypeIds.TypeWithIntersectionMainIntersectionType.toString(),
      boxValueToValue: (value) => value,
      valueToBoxValue: (value) => value,
    );
  }

  const factory TypeWithIntersectionMainIntersectionType({
    required String e,
  }) = _TypeWithIntersectionMainIntersectionType;

  factory TypeWithIntersectionMainIntersectionType.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$TypeWithIntersectionMainIntersectionTypeFromJson(json);
}
class TypeWithIntersection {
  late final List<Object> _values;

  TypeWithIntersection.fromJson(Map<String, dynamic> json){
    this._values = [];
    this._values.add(BasicType.fromJson(json));
    this._values.add(TypeWithIntersectionMainIntersectionType.fromJson(json));
  }

  Map<String, dynamic> toJson(){
    return this._values.map((e) => (e as dynamic).toJson()).reduce((a, b) => a..addAll(b));
  }

  TypeWithIntersection.fromValues({
    required BasicType basicType,
    required TypeWithIntersectionMainIntersectionType typeWithIntersectionMainIntersectionType,
  }){
    _values = [
      basicType,
      typeWithIntersectionMainIntersectionType
    ];
  }

  static ModelsBox<TypeWithIntersection, String> getBox() {
    return ModelsBox<TypeWithIntersection, String>(
      boxKey: HiveTypeIds.TypeWithIntersection.toString(),
      boxValueToValue: (value) => TypeWithIntersection.fromJson(json.decode(value)),
      valueToBoxValue: (value) => json.encode(TypeWithIntersection.toJson()),
    );
  }


  BasicType asBasicType(){
    return this._values[0] as BasicType;
  }
  TypeWithIntersectionMainIntersectionType asTypeWithIntersectionMainIntersectionType(){
    return this._values[1] as TypeWithIntersectionMainIntersectionType;
  }
}

class TypeWithMultipleIntersectionMainIntersectionType with _$TypeWithMultipleIntersectionMainIntersectionType {
  const factory TypeWithMultipleIntersectionMainIntersectionType({
    required String e,
  }) = _TypeWithMultipleIntersectionMainIntersectionType;

  factory TypeWithMultipleIntersectionMainIntersectionType.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$TypeWithMultipleIntersectionMainIntersectionTypeFromJson(json);
}
class TypeWithMultipleIntersection {
  late final List<Object> _values;

  TypeWithMultipleIntersection.fromJson(Map<String, dynamic> json){
    this._values = [];
    this._values.add(BasicType.fromJson(json));
    this._values.add(BasicTypeWithNullableAndOptional.fromJson(json));
    this._values.add(TypeWithMultipleIntersectionMainIntersectionType.fromJson(json));
  }

  Map<String, dynamic> toJson(){
    return this._values.map((e) => (e as dynamic).toJson()).reduce((a, b) => a..addAll(b));
  }

  TypeWithMultipleIntersection.fromValues({
    required BasicType basicType,
    required BasicTypeWithNullableAndOptional basicTypeWithNullableAndOptional,
    required TypeWithMultipleIntersectionMainIntersectionType typeWithMultipleIntersectionMainIntersectionType,
  }){
    _values = [
      basicType,
      basicTypeWithNullableAndOptional,
      typeWithMultipleIntersectionMainIntersectionType
    ];
  }


  BasicType asBasicType(){
    return this._values[0] as BasicType;
  }
  BasicTypeWithNullableAndOptional asBasicTypeWithNullableAndOptional(){
    return this._values[1] as BasicTypeWithNullableAndOptional;
  }
  TypeWithMultipleIntersectionMainIntersectionType asTypeWithMultipleIntersectionMainIntersectionType(){
    return this._values[2] as TypeWithMultipleIntersectionMainIntersectionType;
  }
}

/// Nested type 
@freezed
class NestedType with _$NestedType {
  static ModelsBox<NestedType, NestedType> getBox() {
    return ModelsBox<NestedType, NestedType>(
      boxKey: HiveTypeIds.NestedType.toString(),
      boxValueToValue: (value) => value,
      valueToBoxValue: (value) => value,
    );
  }

  @HiveTypeId(typeId: HiveTypeIds.NestedType)
  const factory NestedType({
    required String a,
    required String b,
    required cAdditionalTypeNestedType c,
  }) = _NestedType;

  factory NestedType.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$NestedTypeFromJson(json);
}


/// additional type of field c from class NestedType 
@freezed
class cAdditionalTypeNestedType with _$cAdditionalTypeNestedType {
  static ModelsBox<cAdditionalTypeNestedType, cAdditionalTypeNestedType> getBox() {
    return ModelsBox<cAdditionalTypeNestedType, cAdditionalTypeNestedType>(
      boxKey: HiveTypeIds.cAdditionalTypeNestedType.toString(),
      boxValueToValue: (value) => value,
      valueToBoxValue: (value) => value,
    );
  }

  @HiveTypeId(typeId: HiveTypeIds.cAdditionalTypeNestedType)
  const factory cAdditionalTypeNestedType({
    required String a,
  }) = _cAdditionalTypeNestedType;

  factory cAdditionalTypeNestedType.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$cAdditionalTypeNestedTypeFromJson(json);
}

/// Simple enum for testing 
enum SimpleEnum{
  one,
  two,
  /// Testing 
  three,
}

/// Enum with defined numbers on options for testing 
enum EnumWithDefinedNumbersOnOptions{
  /// One 
  @JsonValue(1)
  one,
  @JsonValue(2)
  two,
  /// Testing 
  @JsonValue(3)
  three,
}

/// Type with internal enum 
@freezed
class TypeWithInternalEnum with _$TypeWithInternalEnum {
  static ModelsBox<TypeWithInternalEnum, TypeWithInternalEnum> getBox() {
    return ModelsBox<TypeWithInternalEnum, TypeWithInternalEnum>(
      boxKey: HiveTypeIds.TypeWithInternalEnum.toString(),
      boxValueToValue: (value) => value,
      valueToBoxValue: (value) => value,
    );
  }

  @HiveTypeId(typeId: HiveTypeIds.TypeWithInternalEnum)
  const factory TypeWithInternalEnum({
    required String a,
    required String b,
    required cEnum c,
  }) = _TypeWithInternalEnum;

  factory TypeWithInternalEnum.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$TypeWithInternalEnumFromJson(json);
}

@HiveType(typeId: HiveTypeIds.cEnum)
enum cEnum{
  /// One 
  @JsonValue(1)
  @HiveField(1)
  one,
  /// Two 
  @JsonValue(2)
  @HiveField(2)
  two,
}

/// Basic type 
@freezed
class BasicTypeWithFixedEnumField with _$BasicTypeWithFixedEnumField {
  static ModelsBox<BasicTypeWithFixedEnumField, BasicTypeWithFixedEnumField> getBox() {
    return ModelsBox<BasicTypeWithFixedEnumField, BasicTypeWithFixedEnumField>(
      boxKey: HiveTypeIds.BasicTypeWithFixedEnumField.toString(),
      boxValueToValue: (value) => value,
      valueToBoxValue: (value) => value,
    );
  }

  @Assert('b == SimpleEnum.one')
  @HiveTypeId(typeId: HiveTypeIds.BasicTypeWithFixedEnumField)
  const factory BasicTypeWithFixedEnumField({
    /// Basic type a object field comment 
    required String a,
    required SimpleEnum.one b,
  }) = _BasicTypeWithFixedEnumField;

  factory BasicTypeWithFixedEnumField.fromJson(
    Map<String, dynamic> json,
  ) => 
    _$BasicTypeWithFixedEnumFieldFromJson(json);
}
