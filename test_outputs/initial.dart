import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:package:dartz/dartz.dart';
import './hive_type_ids.dart';
import './index.dart';

part 'initial.freezed.dart';
part 'initial.g.dart';

/// Basic type 
@freezed
class BasicType with _$BasicType {
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
@freezed
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
@freezed
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

  bool isBasicType() {
    return _value is BasicType;
  }

  TypeWithUnion asBasicType(){
    return _value as BasicType;
  }

  bool isTypeWithUnionMainUnionType() {
    return _value is TypeWithUnionMainUnionType;
  }

  TypeWithUnion asTypeWithUnionMainUnionType(){
    return _value as TypeWithUnionMainUnionType;
  }

}
@freezed
class TypeWithMultipleUnionMainUnionType with _$TypeWithMultipleUnionMainUnionType {
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

  bool isBasicType() {
    return _value is BasicType;
  }

  TypeWithMultipleUnion asBasicType(){
    return _value as BasicType;
  }

  bool isBasicTypeWithNullableAndOptional() {
    return _value is BasicTypeWithNullableAndOptional;
  }

  TypeWithMultipleUnion asBasicTypeWithNullableAndOptional(){
    return _value as BasicTypeWithNullableAndOptional;
  }

  bool isTypeWithMultipleUnionMainUnionType() {
    return _value is TypeWithMultipleUnionMainUnionType;
  }

  TypeWithMultipleUnion asTypeWithMultipleUnionMainUnionType(){
    return _value as TypeWithMultipleUnionMainUnionType;
  }

}
@freezed
class TypeWithIntersectionMainIntersectionType with _$TypeWithIntersectionMainIntersectionType {
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

  BasicType asBasicType(){
    return this._values[0] as BasicType;
  }
  TypeWithIntersectionMainIntersectionType asTypeWithIntersectionMainIntersectionType(){
    return this._values[1] as TypeWithIntersectionMainIntersectionType;
  }
}
@freezed
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
